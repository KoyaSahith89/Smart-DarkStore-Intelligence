"""
Profit Simulation Engine - Simulates profit impact of business decisions
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection


class ProfitSimulationEngine:
    """Simulate profit impact of various scenarios"""

    def __init__(self):
        self.conn = get_db_connection()

    def calculate_base_metrics(self):
        """Calculate baseline profit metrics"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            a.area_name,
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(o.total_amount) as total_revenue,
            COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' THEN o.order_id END) as fulfilled_orders,
            SUM(d.distance_km) as total_delivery_km
        FROM stores s
        JOIN areas a ON s.area_id = a.area_id
        LEFT JOIN orders o ON s.store_id = o.store_id
        LEFT JOIN deliveries d ON o.order_id = d.order_id
        GROUP BY s.store_id, s.store_name, a.area_name
        """
        df = pd.read_sql_query(query, self.conn)

        if df.empty:
            return df

        # Calculate financial metrics
        df['gross_profit'] = df['total_revenue'] * 0.40  # 40% gross margin
        df['cogs'] = df['total_revenue'] * 0.60
        df['delivery_cost'] = df['total_delivery_km'] * 2  # $2 per km
        df['operational_cost'] = df['total_revenue'] * 0.15  # 15% of revenue
        df['net_profit'] = df['gross_profit'] - df['delivery_cost'] - df['operational_cost']
        df['profit_margin_percentage'] = (df['net_profit'] / df['total_revenue'] * 100).round(2)

        return df

    def simulate_new_store_expansion(self, area_id, estimated_monthly_revenue=50000):
        """Simulate profit impact of opening new store"""
        simulation_results = []

        # Get area details
        cursor = self.conn.cursor()
        cursor.execute("SELECT area_name, population, avg_income FROM areas WHERE area_id = ?", (area_id,))
        area = cursor.fetchone()

        if not area:
            return None

        area_name, population, avg_income = area

        # Assumptions
        monthly_revenue = estimated_monthly_revenue
        gross_margin = 0.40
        delivery_cost_per_km = 2
        avg_delivery_km_per_order = 5
        operational_cost_percentage = 0.15
        monthly_operating_cost = 30000  # Store operations
        initial_investment = 500000

        for month in range(1, 13):
            # Revenue ramps up in first 3 months
            if month <= 3:
                month_revenue = monthly_revenue * (month / 3) * 0.8  # 80% of target
            else:
                month_revenue = monthly_revenue

            orders_estimate = month_revenue / 250  # Average order value $250
            delivery_cost = orders_estimate * avg_delivery_km_per_order * delivery_cost_per_km
            operational_cost = month_revenue * operational_cost_percentage

            gross_profit = month_revenue * gross_margin
            net_profit = gross_profit - delivery_cost - operational_cost - monthly_operating_cost
            cumulative_loss = -initial_investment + (net_profit * month)

            simulation_results.append({
                'month': month,
                'revenue': month_revenue,
                'orders': orders_estimate,
                'gross_profit': gross_profit,
                'delivery_cost': delivery_cost,
                'operational_cost': operational_cost,
                'operating_cost': monthly_operating_cost,
                'net_profit': net_profit,
                'cumulative_profit': cumulative_loss,
                'roi_percentage': (cumulative_loss / initial_investment) * 100 if initial_investment > 0 else 0
            })

        df = pd.DataFrame(simulation_results)
        return {
            'area_name': area_name,
            'area_id': area_id,
            'monthly_revenue': monthly_revenue,
            'initial_investment': initial_investment,
            'simulation': df,
            'payback_month': (initial_investment / (df['net_profit'].mean() + 0.01)) if df['net_profit'].mean() > 0 else float('inf'),
            'year_1_profit': df['net_profit'].sum(),
            'year_1_roi': ((df['net_profit'].sum()) / initial_investment) * 100
        }

    def simulate_pricing_changes(self, price_increase_percentage=10):
        """Simulate profit impact of price changes"""
        base_metrics = self.calculate_base_metrics()

        if base_metrics.empty:
            return base_metrics

        df = base_metrics.copy()

        # Price elasticity assumptions
        elasticity = -1.2  # 1% price increase = 1.2% quantity decrease

        df['new_price_factor'] = 1 + (price_increase_percentage / 100)
        df['demand_change_factor'] = 1 + (elasticity * price_increase_percentage / 100)

        df['new_revenue'] = df['total_revenue'] * df['new_price_factor'] * df['demand_change_factor']
        df['new_gross_profit'] = df['new_revenue'] * 0.40
        df['new_operational_cost'] = df['new_revenue'] * 0.15
        df['new_net_profit'] = df['new_gross_profit'] - df['delivery_cost'] - df['new_operational_cost']

        df['profit_change'] = df['new_net_profit'] - df['net_profit']
        df['profit_change_percentage'] = (df['profit_change'] / df['net_profit'] * 100).round(2)

        return df[['store_id', 'store_name', 'total_revenue', 'new_revenue',
                   'net_profit', 'new_net_profit', 'profit_change', 'profit_change_percentage']]

    def simulate_inventory_reduction(self, reduction_percentage=20):
        """Simulate profit impact of inventory reduction"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            SUM(i.quantity_on_hand * p.unit_price) as current_inventory_value,
            COUNT(DISTINCT i.product_id) as sku_count
        FROM inventory i
        JOIN stores s ON i.store_id = s.store_id
        JOIN products p ON i.product_id = p.product_id
        GROUP BY s.store_id, s.store_name
        """
        df = pd.read_sql_query(query, self.conn)

        if df.empty:
            return df

        # Inventory carrying cost
        carrying_cost_rate = 0.25  # 25% annual

        df['current_carrying_cost'] = df['current_inventory_value'] * carrying_cost_rate
        df['reduced_inventory_value'] = df['current_inventory_value'] * (1 - reduction_percentage / 100)
        df['new_carrying_cost'] = df['reduced_inventory_value'] * carrying_cost_rate
        df['cost_savings'] = df['current_carrying_cost'] - df['new_carrying_cost']

        # Risk factor - potential stockouts
        df['stockout_risk_factor'] = 1 - (reduction_percentage / 100) * 0.5  # Reduce risk by 50% of reduction
        df['profit_impact'] = df['cost_savings'] * df['stockout_risk_factor']

        return df[['store_id', 'store_name', 'current_inventory_value', 'reduced_inventory_value',
                   'current_carrying_cost', 'new_carrying_cost', 'cost_savings', 'profit_impact']]

    def save_simulations_to_db(self):
        """Save all simulations to database"""
        cursor = self.conn.cursor()

        # Get areas for new store simulations
        cursor.execute("SELECT area_id, area_name FROM areas")
        areas = cursor.fetchall()

        for area_id, area_name in areas:
            sim = self.simulate_new_store_expansion(area_id, estimated_monthly_revenue=50000)
            if sim:
                year_1_profit = sim['year_1_profit']
                cursor.execute(
                    """INSERT INTO profit_simulation
                    (scenario_name, scenario_type, area_id, base_profit, 
                     simulated_profit, roi_percentage, assumptions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        f"New Store: {area_name}",
                        'new_store',
                        area_id,
                        0,
                        year_1_profit,
                        sim['year_1_roi'],
                        json.dumps({
                            'monthly_revenue': sim['monthly_revenue'],
                            'initial_investment': sim['initial_investment'],
                            'payback_months': sim['payback_month']
                        })
                    )
                )

        # Pricing change simulation
        pricing_sims = self.simulate_pricing_changes(price_increase_percentage=10)
        for _, row in pricing_sims.iterrows():
            cursor.execute(
                """INSERT INTO profit_simulation
                (scenario_name, scenario_type, store_id, base_profit,
                 simulated_profit, roi_percentage)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    f"10% Price Increase: {row['store_name']}",
                    'pricing_change',
                    int(row['store_id']),
                    row['net_profit'],
                    row['new_net_profit'],
                    (row['profit_change_percentage'] if pd.notna(row['profit_change_percentage']) else 0)
                )
            )

        self.conn.commit()
        print("✓ Saved profit simulation scenarios")

    def close(self):
        """Close database connection"""
        self.conn.close()


def run_profit_simulation():
    """Run profit simulation engine"""
    engine = ProfitSimulationEngine()

    print("\n💵 Profit Simulation Engine")
    print("-" * 60)

    # Save simulations
    engine.save_simulations_to_db()

    # Base metrics
    print("\n📊 Current Store Profitability")
    print("=" * 140)
    base = engine.calculate_base_metrics()
    if not base.empty:
        print(base[['store_id', 'store_name', 'total_revenue', 'net_profit',
                    'profit_margin_percentage']].head(10).to_string(index=False))

    # Pricing simulation
    print("\n💰 Impact of 10% Price Increase")
    print("=" * 140)
    pricing = engine.simulate_pricing_changes(price_increase_percentage=10)
    if not pricing.empty:
        print(pricing.head(10).to_string(index=False))

    # Inventory reduction simulation
    print("\n📦 Impact of 20% Inventory Reduction")
    print("=" * 140)
    inventory = engine.simulate_inventory_reduction(reduction_percentage=20)
    if not inventory.empty:
        print(inventory.to_string(index=False))

    # New store expansion sample
    print("\n🏪 New Store Expansion Simulation (Sample Area)")
    print("=" * 140)
    cursor = engine.conn.cursor()
    cursor.execute("SELECT area_id FROM areas LIMIT 1")
    area_id = cursor.fetchone()
    if area_id:
        sim = engine.simulate_new_store_expansion(area_id[0], estimated_monthly_revenue=50000)
        if sim:
            print(f"\nArea: {sim['area_name']}")
            print(f"Initial Investment: ${sim['initial_investment']:,.0f}")
            print(f"Year 1 Profit: ${sim['year_1_profit']:,.0f}")
            print(f"Year 1 ROI: {sim['year_1_roi']:.2f}%")
            print(f"Payback Period: {sim['payback_month']:.1f} months\n")
            print(sim['simulation'].to_string(index=False))

    engine.close()


if __name__ == "__main__":
    run_profit_simulation()

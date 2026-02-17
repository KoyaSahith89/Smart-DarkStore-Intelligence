"""
Inventory Optimization Engine - Optimizes stock levels using ABC analysis and EOQ
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection


class InventoryOptimizationEngine:
    """Optimize inventory levels and reduce stockouts"""

    def __init__(self):
        self.conn = get_db_connection()

    def abc_analysis(self):
        """Perform ABC analysis on products"""
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            SUM(oi.quantity) as total_quantity_sold,
            SUM(oi.line_total) as total_value,
            COUNT(DISTINCT oi.order_id) as times_ordered
        FROM products p
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_value DESC
        """
        df = pd.read_sql_query(query, self.conn)

        if df.empty:
            return df

        # Calculate cumulative percentage
        df['cumulative_value'] = df['total_value'].cumsum()
        df['cumulative_percentage'] = 100 * df['cumulative_value'] / df['total_value'].sum()

        # Assign ABC categories
        def assign_category(cumulative_pct):
            if cumulative_pct <= 80:
                return 'A'
            elif cumulative_pct <= 95:
                return 'B'
            else:
                return 'C'

        df['abc_category'] = df['cumulative_percentage'].apply(assign_category)
        df = df.drop(['cumulative_value', 'cumulative_percentage'], axis=1)

        return df

    def calculate_reorder_points(self):
        """Calculate optimal reorder points using demand and lead time"""
        query = """
        SELECT 
            i.store_id,
            i.product_id,
            p.product_name,
            i.quantity_on_hand,
            COUNT(DISTINCT CASE WHEN DATE(o.order_date) >= DATE('now', '-30 days') THEN oi.order_id END) as orders_30d,
            SUM(CASE WHEN DATE(o.order_date) >= DATE('now', '-30 days') THEN oi.quantity ELSE 0 END) as quantity_sold_30d,
            s.store_name
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN stores s ON i.store_id = s.store_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.order_id AND o.store_id = s.store_id
        GROUP BY i.store_id, i.product_id, p.product_name, s.store_name
        """
        df = pd.read_sql_query(query, self.conn)

        if df.empty:
            return df

        # Calculate metrics
        df['daily_demand'] = df['quantity_sold_30d'] / 30
        df['lead_time_days'] = 3  # Assume 3-day lead time
        df['safety_stock'] = df['daily_demand'] * 2  # 2 days of safety stock
        df['reorder_point'] = (df['daily_demand'] * df['lead_time_days']) + df['safety_stock']
        df['days_to_stockout'] = df['quantity_on_hand'] / (df['daily_demand'] + 0.001)

        return df[['store_id', 'store_name', 'product_id', 'product_name', 
                   'quantity_on_hand', 'daily_demand', 'reorder_point', 
                   'safety_stock', 'days_to_stockout']]

    def economic_order_quantity(self):
        """Calculate EOQ for optimal ordering"""
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.unit_price,
            SUM(oi.quantity) as annual_demand,
            COUNT(DISTINCT oi.order_id) as number_of_orders
        FROM products p
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.unit_price
        """
        df = pd.read_sql_query(query, self.conn)

        if df.empty:
            return df

        # EOQ Formula: √(2DS/H)
        # D = Annual demand, S = Order cost, H = Holding cost
        order_cost = 100  # $ per order
        holding_cost_rate = 0.25  # 25% of product value per year
        
        df['annual_demand_units'] = df['annual_demand'] * 12  # Scale to annual
        df['holding_cost'] = df['unit_price'] * holding_cost_rate
        df['eoq'] = np.sqrt((2 * df['annual_demand_units'] * order_cost) / (df['holding_cost'] + 0.01))
        df['reorder_frequency_days'] = 365 / (df['annual_demand_units'] / (df['eoq'] + 0.01) + 0.1)

        return df[['product_id', 'product_name', 'unit_price', 'annual_demand_units',
                   'eoq', 'reorder_frequency_days', 'holding_cost']]

    def stockout_risk_analysis(self):
        """Identify products with high stockout risk"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            p.product_id,
            p.product_name,
            p.category,
            i.quantity_on_hand,
            i.reorder_point,
            CASE 
                WHEN i.quantity_on_hand <= i.reorder_point THEN 'CRITICAL'
                WHEN i.quantity_on_hand <= i.reorder_point * 1.5 THEN 'HIGH'
                ELSE 'NORMAL'
            END as risk_level,
            ROUND(100.0 * i.quantity_on_hand / i.reorder_point, 1) as percentage_of_reorder_point
        FROM inventory i
        JOIN stores s ON i.store_id = s.store_id
        JOIN products p ON i.product_id = p.product_id
        WHERE i.quantity_on_hand < i.reorder_point * 2
        ORDER BY risk_level DESC, percentage_of_reorder_point
        """
        return pd.read_sql_query(query, self.conn)

    def inventory_efficiency_metrics(self):
        """Calculate inventory efficiency KPIs"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            COUNT(DISTINCT i.product_id) as total_skus,
            SUM(i.quantity_on_hand) as total_inventory_units,
            ROUND(AVG(i.quantity_on_hand), 2) as avg_units_per_sku,
            SUM(i.quantity_on_hand * p.unit_price) as inventory_value,
            COUNT(DISTINCT CASE WHEN i.quantity_on_hand <= i.reorder_point THEN i.product_id END) as items_below_reorder,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN i.quantity_on_hand <= i.reorder_point THEN i.product_id END) / 
                  COUNT(DISTINCT i.product_id), 2) as percentage_low_stock
        FROM inventory i
        JOIN stores s ON i.store_id = s.store_id
        JOIN products p ON i.product_id = p.product_id
        GROUP BY s.store_id, s.store_name
        ORDER BY percentage_low_stock DESC
        """
        return pd.read_sql_query(query, self.conn)

    def save_optimization_to_db(self):
        """Save optimization recommendations to database"""
        cursor = self.conn.cursor()
        reorder_data = self.calculate_reorder_points()

        for _, row in reorder_data.iterrows():
            cursor.execute(
                """INSERT OR REPLACE INTO inventory_metrics
                (store_id, product_id, metric_date, stock_level, days_to_stockout)
                VALUES (?, ?, DATE('now'), ?, ?)""",
                (int(row['store_id']), int(row['product_id']), 
                 int(row['quantity_on_hand']), int(row['days_to_stockout']))
            )

        self.conn.commit()
        print(f"✓ Saved inventory optimization metrics for {len(reorder_data)} store-product combinations")

    def close(self):
        """Close database connection"""
        self.conn.close()


def run_inventory_optimization():
    """Run inventory optimization engine"""
    engine = InventoryOptimizationEngine()

    print("\n📦 Inventory Optimization Engine")
    print("-" * 60)

    # Save optimization
    engine.save_optimization_to_db()

    # ABC Analysis
    print("\n📊 ABC Analysis (Top 15 by Value)")
    print("=" * 100)
    abc = engine.abc_analysis()
    print(abc.head(15).to_string(index=False))

    # Reorder Points
    print("\n🔄 Recommended Reorder Points (Sample)")
    print("=" * 120)
    reorder = engine.calculate_reorder_points()
    print(reorder.head(10).to_string(index=False))

    # Stockout Risk
    print("\n⚠️  HIGH STOCKOUT RISK ITEMS")
    print("=" * 100)
    risk = engine.stockout_risk_analysis()
    if not risk.empty:
        print(risk.head(15).to_string(index=False))
    else:
        print("No critical stockout risks detected")

    # Inventory Efficiency
    print("\n📈 Store Inventory Efficiency")
    print("=" * 100)
    efficiency = engine.inventory_efficiency_metrics()
    print(efficiency.to_string(index=False))

    engine.close()


if __name__ == "__main__":
    run_inventory_optimization()

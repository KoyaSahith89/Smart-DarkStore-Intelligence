"""
Location Optimization Engine - Identifies best areas for new store placement
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection


class LocationOptimizationEngine:
    """Optimize store locations for maximum revenue and coverage"""

    def __init__(self):
        self.conn = get_db_connection()

    def market_demand_analysis(self):
        """Analyze market demand in different areas"""
        query = """
        SELECT 
            a.area_id,
            a.area_name,
            a.city,
            a.population,
            a.avg_income,
            COUNT(DISTINCT c.customer_id) as registered_customers,
            COUNT(DISTINCT o.order_id) as total_orders,
            ROUND(SUM(o.total_amount), 2) as total_revenue,
            ROUND(AVG(o.total_amount), 2) as avg_order_value,
            COUNT(DISTINCT s.store_id) as existing_stores,
            COUNT(DISTINCT o.order_id) / NULLIF(COUNT(DISTINCT c.customer_id), 0) as orders_per_customer
        FROM areas a
        LEFT JOIN customers c ON a.area_id = c.area_id
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN stores s ON a.area_id = s.area_id
        GROUP BY a.area_id, a.area_name, a.city, a.population, a.avg_income
        ORDER BY total_revenue DESC
        """
        return pd.read_sql_query(query, self.conn)

    def coverage_gap_analysis(self):
        """Identify areas with coverage gaps"""
        query = """
        SELECT 
            a.area_id,
            a.area_name,
            a.city,
            a.population,
            COUNT(DISTINCT s.store_id) as existing_stores,
            a.population / NULLIF(COUNT(DISTINCT s.store_id), 1) as population_per_store,
            COUNT(DISTINCT c.customer_id) as registered_customers,
            COUNT(DISTINCT c.customer_id) / NULLIF(COUNT(DISTINCT s.store_id), 1) as customers_per_store,
            CASE 
                WHEN COUNT(DISTINCT s.store_id) = 0 THEN 'CRITICAL - No Coverage'
                WHEN a.population / COUNT(DISTINCT s.store_id) > 100000 THEN 'HIGH - Severely Underserved'
                WHEN a.population / COUNT(DISTINCT s.store_id) > 50000 THEN 'MEDIUM - Underserved'
                ELSE 'LOW - Adequately Served'
            END as coverage_status,
            CASE 
                WHEN COUNT(DISTINCT s.store_id) = 0 THEN 1
                WHEN a.population / COUNT(DISTINCT s.store_id) > 100000 THEN 2
                WHEN a.population / COUNT(DISTINCT s.store_id) > 50000 THEN 3
                ELSE 4
            END as priority_score
        FROM areas a
        LEFT JOIN stores s ON a.area_id = s.area_id
        LEFT JOIN customers c ON a.area_id = c.area_id
        GROUP BY a.area_id, a.area_name, a.city, a.population
        ORDER BY priority_score ASC
        """
        return pd.read_sql_query(query, self.conn)

    def competitor_analysis(self):
        """Analyze competition in each area"""
        query = """
        SELECT 
            a.area_id,
            a.area_name,
            a.city,
            COUNT(DISTINCT s.store_id) as number_of_stores,
            ROUND(SUM(o.total_amount) / COUNT(DISTINCT s.store_id), 2) as avg_revenue_per_store,
            ROUND(AVG(d.delivery_time_minutes), 2) as avg_delivery_time,
            ROUND(AVG(d.rating), 2) as avg_customer_rating,
            COUNT(DISTINCT c.customer_id) as total_customers,
            ROUND(SUM(o.total_amount), 2) as total_area_revenue
        FROM areas a
        LEFT JOIN stores s ON a.area_id = s.area_id
        LEFT JOIN orders o ON s.store_id = o.store_id
        LEFT JOIN deliveries d ON o.order_id = d.order_id
        LEFT JOIN customers c ON a.area_id = c.area_id
        GROUP BY a.area_id, a.area_name, a.city
        ORDER BY total_area_revenue DESC
        """
        return pd.read_sql_query(query, self.conn)

    def growth_opportunity_scoring(self):
        """Score areas for growth opportunities"""
        demand = self.market_demand_analysis()
        coverage = self.coverage_gap_analysis()

        # Merge data
        df = demand.merge(coverage[['area_id', 'coverage_status', 'priority_score']], on='area_id')

        # Calculate opportunity score (0-100)
        # Factors: population, revenue potential, coverage gap
        max_revenue = demand['total_revenue'].max()
        max_population = demand['population'].max()

        df['revenue_score'] = (df['total_revenue'] / max_revenue) * 30
        df['population_score'] = (df['population'] / max_population) * 30
        df['coverage_score'] = (1 - df['existing_stores'] / (df['existing_stores'].max() + 1)) * 40

        df['opportunity_score'] = df['revenue_score'] + df['population_score'] + df['coverage_score']

        df['recommendation'] = df['opportunity_score'].apply(
            lambda x: 'HIGH PRIORITY' if x > 70 else 'MEDIUM PRIORITY' if x > 50 else 'LOW PRIORITY'
        )

        return df.sort_values('opportunity_score', ascending=False)

    def expansion_roi_estimate(self, store_investment=500000):
        """Estimate ROI for new store expansion"""
        opportunity = self.growth_opportunity_scoring()

        # Conservative estimates
        ramp_up_months = 3
        annual_revenue_estimate = opportunity['total_revenue'] / (opportunity['existing_stores'] + 1)
        profit_margin = 0.15

        opportunity['estimated_annual_revenue'] = annual_revenue_estimate
        opportunity['estimated_annual_profit'] = annual_revenue_estimate * profit_margin
        opportunity['payback_period_months'] = (store_investment / (opportunity['estimated_annual_profit'] / 12 + 0.01))
        opportunity['roi_percentage'] = ((opportunity['estimated_annual_profit'] * 5) / store_investment) * 100

        return opportunity[[
            'area_id', 'area_name', 'city', 'opportunity_score', 'recommendation',
            'existing_stores', 'population', 'total_revenue',
            'estimated_annual_revenue', 'estimated_annual_profit',
            'payback_period_months', 'roi_percentage'
        ]].sort_values('roi_percentage', ascending=False)

    def cluster_analysis(self):
        """Group areas by market characteristics"""
        demand = self.market_demand_analysis()

        if demand.empty:
            return demand

        # Normalize metrics for clustering
        demand['revenue_rank'] = demand['total_revenue'].rank(pct=True)
        demand['income_rank'] = demand['avg_income'].rank(pct=True)
        demand['customer_rank'] = demand['registered_customers'].rank(pct=True)

        # Simple clustering based on characteristics
        def classify_market(row):
            if row['revenue_rank'] > 0.66 and row['income_rank'] > 0.66:
                return 'Premium Market'
            elif row['customer_rank'] > 0.66:
                return 'Mass Market'
            elif row['revenue_rank'] < 0.33:
                return 'Emerging Market'
            else:
                return 'Developing Market'

        demand['market_segment'] = demand.apply(classify_market, axis=1)
        return demand.sort_values('market_segment')

    def save_expansion_recommendations(self):
        """Save expansion recommendations to database"""
        roi_analysis = self.expansion_roi_estimate()
        cursor = self.conn.cursor()

        for _, row in roi_analysis.iterrows():
            if pd.notna(row['area_id']) and row['roi_percentage'] > 30:
                cursor.execute(
                    """INSERT INTO profit_simulation
                    (scenario_name, scenario_type, area_id, roi_percentage, 
                     simulated_profit, assumptions)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        f"New Store in {row['area_name']}",
                        'new_store',
                        int(row['area_id']),
                        row['roi_percentage'],
                        row['estimated_annual_profit'],
                        f"Investment: $500K, Ramp-up: 3 months, Margin: 15%"
                    )
                )

        self.conn.commit()
        print(f"✓ Saved expansion recommendations for high-ROI areas")

    def close(self):
        """Close database connection"""
        self.conn.close()


def run_location_optimization():
    """Run location optimization engine"""
    engine = LocationOptimizationEngine()

    print("\n🗺️  Location Optimization Engine")
    print("-" * 60)

    # Save recommendations
    engine.save_expansion_recommendations()

    # Coverage Gap Analysis
    print("\n📍 Coverage Gap Analysis - Priority Areas")
    print("=" * 120)
    coverage = engine.coverage_gap_analysis()
    print(coverage.head(10).to_string(index=False))

    # Growth Opportunity Scoring
    print("\n🚀 Growth Opportunity Scoring")
    print("=" * 120)
    opportunity = engine.growth_opportunity_scoring()
    print(opportunity.head(10)[['area_id', 'area_name', 'opportunity_score', 'recommendation',
                                 'population', 'total_revenue', 'existing_stores']].to_string(index=False))

    # ROI Estimates
    print("\n💰 Expansion ROI Estimates")
    print("=" * 120)
    roi = engine.expansion_roi_estimate(store_investment=500000)
    print(roi.head(10).to_string(index=False))

    # Market Clustering
    print("\n📊 Market Segmentation")
    print("=" * 120)
    clustering = engine.cluster_analysis()
    print(clustering[['area_name', 'city', 'market_segment', 'population', 'total_revenue']].to_string(index=False))

    engine.close()


if __name__ == "__main__":
    run_location_optimization()

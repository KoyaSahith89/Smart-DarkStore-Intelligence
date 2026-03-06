"""
SQL Analytics Layer - Provides analytical queries for business intelligence
"""
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection


class SQLAnalytics:
    """Analytics queries for Smart DarkStore Intelligence"""

    def __init__(self):
        self.conn = get_db_connection()

    def store_performance_summary(self, days=30):
        """Get store performance metrics"""
        query = f"""
        SELECT 
            s.store_id,
            s.store_name,
            a.area_name,
            COUNT(DISTINCT o.order_id) as total_orders,
            ROUND(SUM(o.total_amount), 2) as total_revenue,
            ROUND(AVG(o.total_amount), 2) as avg_order_value,
            COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' THEN o.order_id END) as delivered_orders,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' THEN o.order_id END) / 
                  COUNT(DISTINCT o.order_id), 2) as order_fulfillment_rate,
            ROUND(AVG(d.delivery_time_minutes), 2) as avg_delivery_time_minutes,
            COUNT(DISTINCT CASE WHEN d.rating >= 4 THEN d.delivery_id END) as high_rated_deliveries
        FROM stores s
        JOIN areas a ON s.area_id = a.area_id
        LEFT JOIN orders o ON s.store_id = o.store_id 
            AND DATE(o.order_date) >= DATE('now', '-{days} days')
        LEFT JOIN deliveries d ON o.order_id = d.order_id
        GROUP BY s.store_id, s.store_name, a.area_name
        ORDER BY total_revenue DESC
        """
        return pd.read_sql_query(query, self.conn)

    def area_demand_analysis(self):
        """Analyze demand by area"""
        query = """
        SELECT 
            a.area_id,
            a.area_name,
            a.city,
            COUNT(DISTINCT c.customer_id) as total_customers,
            COUNT(DISTINCT o.order_id) as total_orders,
            ROUND(SUM(o.total_amount), 2) as area_revenue,
            ROUND(AVG(o.total_amount), 2) as avg_order_value,
            COUNT(DISTINCT o.order_id) / COUNT(DISTINCT c.customer_id) as orders_per_customer,
            a.population,
            ROUND(1000000.0 * SUM(o.total_amount) / a.population, 2) as revenue_per_million_population
        FROM areas a
        LEFT JOIN customers c ON a.area_id = c.area_id
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY a.area_id, a.area_name, a.city, a.population
        ORDER BY area_revenue DESC
        """
        return pd.read_sql_query(query, self.conn)

    def product_sales_analysis(self):
        """Analyze product performance"""
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            p.unit_price,
            COUNT(DISTINCT oi.order_id) as times_ordered,
            SUM(oi.quantity) as total_quantity_sold,
            ROUND(SUM(oi.line_total), 2) as total_revenue,
            ROUND(AVG(oi.quantity), 2) as avg_quantity_per_order,
            ROUND(100.0 * SUM(oi.quantity) / (SELECT SUM(quantity) FROM order_items), 2) as sales_percentage
        FROM products p
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.category, p.unit_price
        ORDER BY total_revenue DESC
        """
        return pd.read_sql_query(query, self.conn)

    def inventory_status(self):
        """Check inventory levels and stockout risks"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            p.product_id,
            p.product_name,
            i.quantity_on_hand,
            i.reorder_point,
            i.max_stock,
            CASE 
                WHEN i.quantity_on_hand <= i.reorder_point THEN 'CRITICAL - Reorder Now'
                WHEN i.quantity_on_hand <= i.reorder_point * 1.5 THEN 'LOW - Monitor'
                WHEN i.quantity_on_hand > i.max_stock * 0.8 THEN 'HIGH - Consider Promotion'
                ELSE 'NORMAL'
            END as inventory_status,
            ROUND(100.0 * i.quantity_on_hand / i.max_stock, 2) as stock_percentage
        FROM stores s
        JOIN inventory i ON s.store_id = i.store_id
        JOIN products p ON i.product_id = p.product_id
        WHERE i.quantity_on_hand <= i.reorder_point * 2
        ORDER BY s.store_id, inventory_status DESC
        """
        return pd.read_sql_query(query, self.conn)

    def delivery_performance_sla(self, target_minutes=30):
        """Measure SLA compliance"""
        query = f"""
        SELECT 
            s.store_id,
            s.store_name,
            a.area_name,
            COUNT(d.delivery_id) as total_deliveries,
            COUNT(CASE WHEN d.delivery_status = 'delivered' THEN 1 END) as completed_deliveries,
            COUNT(CASE WHEN d.delivery_time_minutes <= {target_minutes} THEN 1 END) as on_time_deliveries,
            ROUND(100.0 * COUNT(CASE WHEN d.delivery_time_minutes <= {target_minutes} THEN 1 END) / 
                  COUNT(d.delivery_id), 2) as sla_compliance_percentage,
            ROUND(AVG(d.delivery_time_minutes), 2) as avg_delivery_time,
            ROUND(AVG(d.rating), 2) as avg_rating,
            COUNT(CASE WHEN d.rating >= 4.5 THEN 1 END) as excellent_ratings
        FROM stores s
        JOIN areas a ON s.area_id = a.area_id
        LEFT JOIN deliveries d ON s.store_id = d.store_id
        GROUP BY s.store_id, s.store_name, a.area_name
        ORDER BY sla_compliance_percentage DESC
        """
        return pd.read_sql_query(query, self.conn)

    def customer_insights(self):
        """Analyze customer behavior"""
        query = """
        SELECT 
            c.customer_id,
            c.customer_name,
            a.area_name,
            COUNT(o.order_id) as order_count,
            ROUND(SUM(o.total_amount), 2) as lifetime_value,
            ROUND(AVG(o.total_amount), 2) as avg_order_value,
            ROUND(julianday('now') - julianday(MAX(o.order_date)), 0) as days_since_last_order,
            CASE 
                WHEN COUNT(o.order_id) >= 10 THEN 'VIP'
                WHEN COUNT(o.order_id) >= 5 THEN 'Regular'
                ELSE 'New'
            END as customer_segment
        FROM customers c
        LEFT JOIN areas a ON c.area_id = a.area_id
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name, a.area_name
        ORDER BY lifetime_value DESC
        """
        return pd.read_sql_query(query, self.conn)

    def peak_demand_hours(self):
        """Find peak order hours"""
        query = """
        SELECT 
            CAST(strftime('%H', o.order_time) AS INTEGER) as order_hour,
            COUNT(o.order_id) as order_count,
            ROUND(SUM(o.total_amount), 2) as hour_revenue,
            ROUND(AVG(o.total_amount), 2) as avg_order_value
        FROM orders o
        GROUP BY CAST(strftime('%H', o.order_time) AS INTEGER)
        ORDER BY order_count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def area_expansion_opportunity(self):
        """Identify best areas for new store expansion"""
        query = """
        SELECT 
            a.area_id,
            a.area_name,
            a.city,
            a.population,
            COUNT(DISTINCT c.customer_id) as customers_in_area,
            COUNT(DISTINCT s.store_id) as existing_stores,
            ROUND(a.population / NULLIF(COUNT(DISTINCT s.store_id), 0), 0) as population_per_store,
            ROUND(SUM(o.total_amount), 2) as area_revenue,
            ROUND(SUM(o.total_amount) / NULLIF(COUNT(DISTINCT s.store_id), 1), 2) as revenue_per_store,
            CASE 
                WHEN COUNT(DISTINCT s.store_id) = 0 THEN 'CRITICAL - No Store'
                WHEN a.population / COUNT(DISTINCT s.store_id) > 100000 THEN 'HIGH - Underserved'
                WHEN a.population / COUNT(DISTINCT s.store_id) > 50000 THEN 'MEDIUM - Growth Opportunity'
                ELSE 'LOW - Adequately Served'
            END as expansion_priority
        FROM areas a
        LEFT JOIN customers c ON a.area_id = c.area_id
        LEFT JOIN stores s ON a.area_id = s.area_id
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY a.area_id, a.area_name, a.city, a.population
        ORDER BY expansion_priority DESC
        """
        return pd.read_sql_query(query, self.conn)

    def profitability_by_store(self):
        """Calculate profitability metrics"""
        query = """
        SELECT 
            s.store_id,
            s.store_name,
            a.area_name,
            COUNT(DISTINCT o.order_id) as total_orders,
            ROUND(SUM(o.total_amount), 2) as total_revenue,
            ROUND(SUM(d.distance_km), 2) as total_delivery_km,
            ROUND(AVG(d.delivery_time_minutes), 2) as avg_delivery_time,
            ROUND(SUM(o.total_amount) * 0.15, 2) as estimated_gross_profit,  -- Assuming 15% margin
            ROUND(SUM(o.total_amount) * 0.15 - (SUM(d.distance_km) * 2), 2) as estimated_net_profit  -- $2 per km delivery cost
        FROM stores s
        JOIN areas a ON s.area_id = a.area_id
        LEFT JOIN orders o ON s.store_id = o.store_id
        LEFT JOIN deliveries d ON o.order_id = d.order_id
        GROUP BY s.store_id, s.store_name, a.area_name
        ORDER BY estimated_net_profit DESC
        """
        return pd.read_sql_query(query, self.conn)

    def close(self):
        """Close database connection"""
        self.conn.close()


def print_analytics():
    """Print all analytics reports"""
    analytics = SQLAnalytics()

    print("\n" + "="*80)
    print("STORE PERFORMANCE SUMMARY (Last 30 days)")
    print("="*80)
    print(analytics.store_performance_summary(days=30).to_string(index=False))

    print("\n" + "="*80)
    print("AREA DEMAND ANALYSIS")
    print("="*80)
    print(analytics.area_demand_analysis().to_string(index=False))

    print("\n" + "="*80)
    print("TOP PRODUCTS BY REVENUE")
    print("="*80)
    print(analytics.product_sales_analysis().head(10).to_string(index=False))

    print("\n" + "="*80)
    print("DELIVERY PERFORMANCE & SLA")
    print("="*80)
    print(analytics.delivery_performance_sla(target_minutes=30).to_string(index=False))

    print("\n" + "="*80)
    print("INVENTORY STATUS ALERTS")
    print("="*80)
    print(analytics.inventory_status().head(20).to_string(index=False))

    print("\n" + "="*80)
    print("PEAK DEMAND HOURS")
    print("="*80)
    print(analytics.peak_demand_hours().to_string(index=False))

    print("\n" + "="*80)
    print("AREA EXPANSION OPPORTUNITIES")
    print("="*80)
    print(analytics.area_expansion_opportunity().to_string(index=False))

    print("\n" + "="*80)
    print("STORE PROFITABILITY")
    print("="*80)
    print(analytics.profitability_by_store().to_string(index=False))

    analytics.close()


if __name__ == "__main__":
    print_analytics()

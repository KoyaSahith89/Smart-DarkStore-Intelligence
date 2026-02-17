import sqlite3
from sqlite3 import Connection
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "darkstore.db"


def get_db_connection() -> Connection:
    """Get SQLite database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    """Create all tables in SQLite database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables (for development)
    tables = [
        "deliveries", "orders", "inventory", "order_items",
        "customers", "products", "stores", "areas", "store_metrics",
        "delivery_metrics", "inventory_metrics", "demand_forecast",
        "delivery_predictions", "profit_simulation"
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Areas Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            area_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            population INTEGER,
            avg_income REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Stores Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id INTEGER NOT NULL,
            store_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            warehouse_size INTEGER,  -- in sq meters
            staff_count INTEGER,
            operational_hours TEXT,  -- e.g., "8 AM - 12 AM"
            opening_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (area_id) REFERENCES areas(area_id)
        )
    """)

    # Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            unit_price REAL NOT NULL,
            supplier_id TEXT,
            shelf_life INTEGER,  -- in days
            weight REAL,  -- in kg
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Customers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            registration_date DATE,
            lifetime_orders INTEGER DEFAULT 0,
            lifetime_value REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (area_id) REFERENCES areas(area_id)
        )
    """)

    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,
            order_date TIMESTAMP NOT NULL,
            order_time TIME,
            total_amount REAL NOT NULL,
            order_status TEXT,  -- "pending", "confirmed", "delivered", "cancelled"
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (store_id) REFERENCES stores(store_id)
        )
    """)

    # Order Items Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            line_total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity_on_hand INTEGER NOT NULL,
            reorder_point INTEGER,
            max_stock INTEGER,
            last_restocked TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store_id, product_id),
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # Deliveries Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deliveries (
            delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            delivery_address TEXT,
            scheduled_delivery_time TIMESTAMP,
            actual_delivery_time TIMESTAMP,
            delivery_status TEXT,  -- "pending", "picked_up", "in_transit", "delivered", "failed"
            delivery_time_minutes INTEGER,
            distance_km REAL,
            delivery_partner TEXT,
            rating REAL,  -- 1-5 stars
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)

    # Store Metrics Table (for analytics)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            metric_date DATE NOT NULL,
            daily_revenue REAL,
            daily_orders INTEGER,
            avg_order_value REAL,
            inventory_turnover REAL,
            stockout_events INTEGER,
            customer_satisfaction REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store_id, metric_date),
            FOREIGN KEY (store_id) REFERENCES stores(store_id)
        )
    """)

    # Delivery Metrics Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS delivery_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            metric_date DATE NOT NULL,
            total_deliveries INTEGER,
            on_time_deliveries INTEGER,
            avg_delivery_time REAL,
            delivery_cost REAL,
            sla_compliance REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store_id, metric_date),
            FOREIGN KEY (store_id) REFERENCES stores(store_id)
        )
    """)

    # Inventory Metrics Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            metric_date DATE NOT NULL,
            abc_category TEXT,  -- "A", "B", "C"
            stock_level INTEGER,
            days_to_stockout REAL,
            safety_stock INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store_id, product_id, metric_date),
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # Demand Forecast Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demand_forecast (
            forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            forecast_date DATE NOT NULL,
            forecasted_quantity INTEGER,
            forecast_model TEXT,  -- "arima", "prophet", "ml"
            confidence_interval_lower INTEGER,
            confidence_interval_upper INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store_id, product_id, forecast_date),
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # Delivery Time Predictions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS delivery_predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            area_id INTEGER NOT NULL,
            order_hour INTEGER,
            day_of_week INTEGER,
            predicted_delivery_time REAL,  -- in minutes
            confidence_score REAL,  -- 0-1
            model_version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(store_id, area_id, order_hour, day_of_week),
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (area_id) REFERENCES areas(area_id)
        )
    """)

    # Profit Simulation Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profit_simulation (
            simulation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_name TEXT NOT NULL,
            scenario_type TEXT,  -- "new_store", "pricing_change", "inventory_reduction"
            store_id INTEGER,
            area_id INTEGER,
            base_profit REAL,
            simulated_profit REAL,
            profit_difference REAL,
            roi_percentage REAL,
            assumptions TEXT,  -- JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (store_id) REFERENCES stores(store_id),
            FOREIGN KEY (area_id) REFERENCES areas(area_id)
        )
    """)

    conn.commit()
    conn.close()
    print("✓ Database schema created successfully!")


if __name__ == "__main__":
    create_database()

"""
Data Simulation Engine - Generates realistic darkstore data
"""
import random
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_schema import get_db_connection


def generate_areas(count=5):
    """Generate area data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    areas_data = [
        ("Downtown", "Mumbai", 19.0760, 72.8777, 500000, 45000),
        ("Suburban North", "Mumbai", 19.2183, 72.8397, 300000, 35000),
        ("Suburban South", "Mumbai", 19.0176, 72.8479, 350000, 38000),
        ("Tech Park", "Bangalore", 12.9716, 77.5946, 200000, 55000),
        ("IT Corridor", "Bangalore", 12.9352, 77.6245, 250000, 60000),
    ]

    for area in areas_data[:count]:
        cursor.execute(
            "INSERT INTO areas (area_name, city, latitude, longitude, population, avg_income) VALUES (?, ?, ?, ?, ?, ?)",
            area
        )

    conn.commit()
    conn.close()
    print(f"✓ Generated {count} areas")


def generate_stores(areas_per_city=2):
    """Generate store data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all areas
    cursor.execute("SELECT area_id, area_name FROM areas")
    areas = cursor.fetchall()

    store_counter = 1
    for area_id, area_name in areas:
        for i in range(areas_per_city):
            store_name = f"{area_name} Store {i+1}"
            latitude = float(random.uniform(-0.01, 0.01)) + 19.0  # Add slight variation
            longitude = float(random.uniform(-0.01, 0.01)) + 72.8
            warehouse_size = random.randint(5000, 50000)  # sq meters
            staff_count = random.randint(50, 200)
            operational_hours = "8 AM - 12 AM"
            opening_date = (datetime.now() - timedelta(days=random.randint(30, 365))).date()

            cursor.execute(
                """INSERT INTO stores 
                (area_id, store_name, latitude, longitude, warehouse_size, staff_count, operational_hours, opening_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (area_id, store_name, latitude, longitude, warehouse_size, staff_count, operational_hours, opening_date)
            )
            store_counter += 1

    conn.commit()
    conn.close()
    print(f"✓ Generated {store_counter - 1} stores")


def generate_products(count=50):
    """Generate product data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    categories = ["Groceries", "Beverages", "Dairy", "Snacks", "Frozen", "Personal Care", "Electronics"]
    product_names = {
        "Groceries": ["Rice", "Wheat", "Sugar", "Salt", "Oil", "Flour"],
        "Beverages": ["Water Bottle", "Cold Drink", "Juice", "Tea", "Coffee"],
        "Dairy": ["Milk", "Yogurt", "Cheese", "Butter", "Cream"],
        "Snacks": ["Chips", "Cookies", "Nuts", "Biscuits", "Crackers"],
        "Frozen": ["Ice Cream", "Frozen Pizza", "Frozen Vegetables", "Ice"],
        "Personal Care": ["Shampoo", "Soap", "Toothpaste", "Deodorant", "Face Wash"],
        "Electronics": ["Phone Charger", "USB Cable", "Power Bank", "Headphones"]
    }

    products_inserted = 0
    for category in categories:
        for product_name in product_names[category]:
            unit_price = round(random.uniform(10, 500), 2)
            shelf_life = random.randint(7, 365)
            weight = round(random.uniform(0.1, 10), 2)

            cursor.execute(
                """INSERT INTO products 
                (product_name, category, unit_price, shelf_life, weight)
                VALUES (?, ?, ?, ?, ?)""",
                (product_name, category, unit_price, shelf_life, weight)
            )
            products_inserted += 1
            if products_inserted >= count:
                break
        if products_inserted >= count:
            break

    conn.commit()
    conn.close()
    print(f"✓ Generated {products_inserted} products")


def generate_customers(per_area=100):
    """Generate customer data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT area_id FROM areas")
    areas = cursor.fetchall()

    first_names = ["Raj", "Priya", "Amit", "Neha", "Vikram", "Anjali", "Arjun", "Divya"]
    last_names = ["Sharma", "Singh", "Patel", "Khan", "Gupta", "Kumar", "Reddy", "Verma"]

    customer_count = 0
    for (area_id,) in areas:
        for _ in range(per_area):
            customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            email = f"{customer_name.lower().replace(' ', '_')}{random.randint(1, 999)}@email.com"
            phone = f"+91{random.randint(6000000000, 9999999999)}"
            address = f"{random.randint(100, 9999)} {random.choice(['Main St', 'Park Ave', 'Oak Rd', 'Hill St'])}"
            registration_date = (datetime.now() - timedelta(days=random.randint(1, 730))).date()

            cursor.execute(
                """INSERT INTO customers 
                (area_id, customer_name, email, phone, address, registration_date)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (area_id, customer_name, email, phone, address, registration_date)
            )
            customer_count += 1

    conn.commit()
    conn.close()
    print(f"✓ Generated {customer_count} customers")


def generate_orders(days=30, orders_per_day=100):
    """Generate order data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id, area_id FROM customers")
    customers = cursor.fetchall()

    cursor.execute("SELECT store_id, area_id FROM stores")
    stores = cursor.fetchall()

    cursor.execute("SELECT product_id FROM products")
    products = [row[0] for row in cursor.fetchall()]

    order_statuses = ["pending", "confirmed", "delivered", "cancelled"]
    orders_inserted = 0

    for day_offset in range(days):
        order_date = (datetime.now() - timedelta(days=day_offset)).date()

        for _ in range(orders_per_day):
            # Random customer
            customer_id, customer_area = random.choice(customers)

            # Store should preferably be in same area
            same_area_stores = [s for s in stores if s[1] == customer_area]
            store_id = random.choice(same_area_stores)[0] if same_area_stores else random.choice(stores)[0]

            order_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00"
            order_datetime = datetime.combine(order_date, datetime.strptime(order_time, "%H:%M:%S").time())

            # Generate random items
            num_items = random.randint(1, 5)
            total_amount = 0
            order_id_temp = None

            cursor.execute(
                """INSERT INTO orders 
                (customer_id, store_id, order_date, order_time, total_amount, order_status)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (customer_id, store_id, order_datetime, order_time, 0, random.choice(order_statuses))
            )

            order_id_temp = cursor.lastrowid

            # Add order items
            for _ in range(num_items):
                product_id = random.choice(products)
                quantity = random.randint(1, 5)

                cursor.execute("SELECT unit_price FROM products WHERE product_id = ?", (product_id,))
                unit_price = cursor.fetchone()[0]

                line_total = quantity * unit_price
                total_amount += line_total

                cursor.execute(
                    """INSERT INTO order_items 
                    (order_id, product_id, quantity, unit_price, line_total)
                    VALUES (?, ?, ?, ?, ?)""",
                    (order_id_temp, product_id, quantity, unit_price, line_total)
                )

            # Update total amount
            cursor.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", (total_amount, order_id_temp))
            orders_inserted += 1

    conn.commit()
    conn.close()
    print(f"✓ Generated {orders_inserted} orders")


def generate_deliveries():
    """Generate delivery data based on orders"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.order_id, o.customer_id, o.store_id, o.order_date, c.address
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_status IN ('delivered', 'confirmed')
    """)
    orders = cursor.fetchall()

    delivery_statuses = ["delivered", "in_transit", "picked_up", "pending"]
    delivery_partners = ["FreshExpress", "QuickDeliver", "SpeedHub", "LocalLogistics"]

    for order_id, customer_id, store_id, order_date, address in orders:
        scheduled_time = datetime.combine(
            datetime.fromisoformat(str(order_date)).date(),
            datetime.strptime(f"{random.randint(8, 23):02d}:{random.randint(0, 59):02d}:00", "%H:%M:%S").time()
        )

        actual_time = scheduled_time + timedelta(minutes=random.randint(-30, 60))
        delivery_time = (actual_time - datetime.fromisoformat(str(order_date))).total_seconds() / 60

        distance_km = round(random.uniform(1, 15), 2)
        status = random.choice(delivery_statuses)
        rating = round(random.uniform(3.5, 5.0), 1) if status == "delivered" else None

        cursor.execute(
            """INSERT INTO deliveries 
            (order_id, store_id, customer_id, delivery_address, scheduled_delivery_time, 
             actual_delivery_time, delivery_status, delivery_time_minutes, distance_km, 
             delivery_partner, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (order_id, store_id, customer_id, address, scheduled_time, actual_time,
             status, int(delivery_time), distance_km, random.choice(delivery_partners), rating)
        )

    conn.commit()
    conn.close()
    print(f"✓ Generated {len(orders)} deliveries")


def generate_inventory():
    """Generate inventory data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT store_id FROM stores")
    stores = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT product_id FROM products")
    products = [row[0] for row in cursor.fetchall()]

    for store_id in stores:
        for product_id in products:
            quantity_on_hand = random.randint(10, 1000)
            reorder_point = random.randint(20, 100)
            max_stock = reorder_point * 10

            cursor.execute(
                """INSERT INTO inventory 
                (store_id, product_id, quantity_on_hand, reorder_point, max_stock, last_restocked)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (store_id, product_id, quantity_on_hand, reorder_point, max_stock, datetime.now())
            )

    conn.commit()
    conn.close()
    print(f"✓ Generated inventory for {len(stores)} stores × {len(products)} products")


def simulate_all():
    """Run all data simulation"""
    print("\n🚀 Starting Data Simulation Engine...\n")
    generate_areas(count=5)
    generate_stores(areas_per_city=2)
    generate_products(count=50)
    generate_customers(per_area=50)
    generate_orders(days=30, orders_per_day=50)
    generate_deliveries()
    generate_inventory()
    print("\n✓ Data Simulation Complete!\n")


if __name__ == "__main__":
    simulate_all()

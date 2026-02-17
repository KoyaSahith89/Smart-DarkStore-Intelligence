import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine

fake = Faker()

# Connect to SQLite database
engine = create_engine('sqlite:///darkstore.db')

# Load existing stores and products from the database
stores_df = pd.read_sql('SELECT * FROM stores', engine)
products_df = pd.read_sql('SELECT * FROM products', engine)

# Preview first 5 rows to confirm
print("Stores preview:")
print(stores_df.head())

print("\nProducts preview:")
print(products_df.head())
print("Products columns:", products_df.columns)

# Number of orders to generate
num_orders = 2000

orders_list = []

for i in range(num_orders):
    order_id = i + 1
    # Random store
    store_id = stores_df.sample(1)['store_id'].values[0]
    # Random product
    product_name = products_df.sample(1)['product_name'].values[0]
    # Random quantity (1 to 5 units)
    quantity = np.random.randint(1, 6)
    # Random order timestamp within last 30 days
    order_timestamp = fake.date_time_between(start_date='-30d', end_date='now')

    orders_list.append({
        'order_id': order_id,
        'store_id': store_id,
        'product_name': product_name,
        'quantity': quantity,
        'order_timestamp': order_timestamp
    })

# Convert to DataFrame
orders_df = pd.DataFrame(orders_list)

# Preview first 5 orders
print("Orders preview:")
print(orders_df.head())
# Save orders to database
orders_df.to_sql('orders', engine, if_exists='replace', index=False)
print("Orders table saved successfully!")

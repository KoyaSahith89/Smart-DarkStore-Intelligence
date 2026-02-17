

import sqlite3
from generate_areas import generate_areas
from generate_products import generate_products
from generate_stores import generate_stores  # Import your store generator

def save_all_to_db(db_name="darkstore.db"):
    conn = sqlite3.connect(db_name)

    # Generate data
    areas_df = generate_areas()
    products_df = generate_products()
    stores_df = generate_stores()  # Generate stores DataFrame

    # Save to database
    areas_df.to_sql("areas", conn, if_exists="replace", index=False)
    products_df.to_sql("products", conn, if_exists="replace", index=False)
    stores_df.to_sql("stores", conn, if_exists="replace", index=False)

    conn.close()
    print("Areas, Products, and Stores tables saved successfully!")

if __name__ == "__main__":
    save_all_to_db()


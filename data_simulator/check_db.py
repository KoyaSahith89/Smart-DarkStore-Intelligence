
import sqlite3
import pandas as pd

def check_areas(db_name="darkstore.db"):
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM areas LIMIT 5;"
    df = pd.read_sql(query, conn)
    conn.close()
    print("----- Areas -----")
    print(df)

def check_stores(db_name="darkstore.db"):
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM stores LIMIT 5;"
    df = pd.read_sql(query, conn)
    conn.close()
    print("\n----- Stores -----")
    print(df)

    # Optional: stores per area
    area_counts = df['area_id'].value_counts()
    print("\nNumber of stores per area:")
    print(area_counts)

def check_orders(db_name="darkstore.db"):
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM orders LIMIT 5;"
    df = pd.read_sql(query, conn)
    conn.close()
    print("\n----- Orders -----")
    print(df)

    # Optional: count of orders per store
    store_counts = df['store_id'].value_counts()
    print("\nNumber of orders per store (in preview):")
    print(store_counts)


if __name__ == "__main__":
    check_areas()
    check_stores()
    check_orders()

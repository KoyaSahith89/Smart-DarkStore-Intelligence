# data_simulator/generate_stores.py

import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine

fake = Faker()

def generate_stores(num_stores=20):
    """Generates a DataFrame of stores linked to areas"""
    # Connect to your DB to get areas
    engine = create_engine('sqlite:///darkstore.db')
    areas_df = pd.read_sql('SELECT * FROM areas', engine)

    stores_list = []
    for i in range(num_stores):
        store_id = i + 1
        store_name = fake.company()
        area_id = areas_df.sample(1)['area_id'].values[0]
        capacity = np.random.randint(50, 201)
        stores_list.append({
            'store_id': store_id,
            'store_name': store_name,
            'area_id': area_id,
            'capacity': capacity
        })

    stores_df = pd.DataFrame(stores_list)
    return stores_df

# Optional: allow running standalone
if __name__ == "__main__":
    df = generate_stores()
    print(df.head())

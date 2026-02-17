import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_areas(n_areas=50):
    areas = []

    for i in range(1, n_areas + 1):
        area = {
            "area_id": i,
            "area_name": fake.city(),
            "population_density": random.randint(5000, 30000),
            "avg_income": random.randint(20000, 150000),
            "commercial_score": round(random.uniform(0.5, 1.5), 2)
        }
        areas.append(area)

    df = pd.DataFrame(areas)
    return df


if __name__ == "__main__":
    df = generate_areas()
    print(df.head())

import pandas as pd
from sqlalchemy import create_engine

# Connect to SQLite database
engine = create_engine('sqlite:///darkstore.db')

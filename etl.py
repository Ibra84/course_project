import pandas as pd
from connector import get_connection

def get_data(query):
    conn = get_connection()
    df = conn.execute(query).fetchdf()
    conn.close()
    return df




import duckdb

def get_connection(db_path='my.db'):
    return duckdb.connect(db_path)

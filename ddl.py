import duckdb
import os

def execute_query_from_file(conn, file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"SQL file not found: {file_path}")
    with open(file_path, 'r') as file:
        query = file.read()
    conn.execute(query)

def load_data_from_csv(conn, table_name, csv_file):
    # Загрузка данных из CSV файла в таблицу
    query = f"""
    INSERT INTO {table_name}
    SELECT * FROM read_csv_auto('{csv_file}')
    """
    conn.execute(query)
    print(f"Data loaded into table {table_name} from {csv_file}")

def initialize_database(db_path='my.db'):
    # Создаем или открываем файл базы данных
    conn = duckdb.connect(db_path)
    
    # Выполнение SQL скриптов для создания таблиц и вьюшек
    execute_query_from_file(conn, 'queries/create_tables.sql')
    execute_query_from_file(conn, 'queries/create_views.sql')
    execute_query_from_file(conn, 'queries/queries.sql')
    
    # Заполнение таблиц данными из CSV файлов
    try:
        load_data_from_csv(conn, 'products', 'source/products.csv')
        load_data_from_csv(conn, 'regions', 'source/regions.csv')
        load_data_from_csv(conn, 'sales', 'source/sales.csv')
        print("CSV data loaded successfully.")
    except Exception as e:
        print(f"Error while loading CSV data: {e}")
    
    # Закрываем соединение
    conn.close()

# Пример использования
if __name__ == "__main__":
    try:
        initialize_database()
        print("Database initialized successfully.")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

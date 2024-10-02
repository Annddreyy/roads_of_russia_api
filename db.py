import pyodbc

def get_connection():
    SERVER = 'localhost'
    DATABASE = 'roads_of_russia'
    USERNAME = 'sa'
    PASSWORD = '1234'
    connectionString = (f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                        f'SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
                        f'Trusted_Connection=yes')

    conn = pyodbc.connect(connectionString)

    return conn

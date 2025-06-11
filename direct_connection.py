import pyodbc

server = 'SK-INSPIRON-3K\MSSQLSERVER01' 
database = 'Chinook'
username = ''        
password = ''        
driver = '{ODBC Driver 17 for SQL Server}'  

# For Windows Authentication:
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# For SQL Server Authentication:
#conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print("Connected successfully. SQL Server version:")
    print(row[0])
    #conn.close()
except Exception as e:
    print("Connection failed:", e)

# GWS-pyspark-task
GWS pyspark task

A Python-based interface to interact with various SQL databases, including SQL Server, PostgreSQL, MySQL, and SQLite. This project abstracts database operations, allowing for seamless integration and management.

## Features

- Connect to different SQL databases
- Execute queries: SELECT, INSERT, UPDATE, DELETE
- Bulk upsert operations
- Following operations are defined:
    connect
    read
    stream_read
    insert
    bulk_upsert
    update
    execute - create, update, delete, drop, call procedure
    close
    sql server conn handler


## Installation

1. Clone the repository:

git clone https://github.com/oxerz8/GWS-pyspark-task.git
cd GWS-pyspark-task

2. Install the required packages:
pip install -r requirements.txt

3. Open python in the above folder.
python

## Example usage
### Read
```python
from source.interface_class import *
sql_server = SQLServerDB(server='SK-INSPIRON-3K\\MSSQLSERVER01', database='Chinook')
sql_server.connect()
data = sql_server.read("Track")
print(data)
sql_server.close()
```
### Stream_read
```python
sql_server.connect()
sql_server.stream_read('Track', 2)
sql_server.close()
```
### Insert
```python
sql_server.connect()
params = (4,'Dano',29)
sql_server.insert('sampletable', params)
sql_server.close()
```
### Update
```python
sql_server.connect()
sql_server.update(
    table='sampletable',
    updates={'age': 32},
    condition='name = ?',
    condition_params=('Alice',)
)
sql_server.close()
```

### Upsert
```python
sql_server.connect()
# Define the columns in the table
columns = ['id', 'name', 'age']

# Data to insert or update
params = [
    (1, 'Alice', 30),
    (2, 'Bob', 22),
    (3, 'Charlie', 28)
]

# Call the method
sql_server.bulk_upsert('sampletable', columns, match_column='id', params_list=params)

sql_server.close()
```
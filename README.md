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

def use_database(db: BaseDBInterface):
    db.connect()
    data = db.read("SELECT * FROM Track")
    print(data)
    db.close()

sql_server = SQLServerDB(server='SK-INSPIRON-3K\\MSSQLSERVER01', database='Chinook')
# This will print the table Track.
use_database(sql_server)
```
### Stream_read
```python
sql_server.connect()
sql_server.stream_read('SELECT * FROM Track', 2)
sql_server.close()
```
### Insert
```python
sql_server.connect()
query = 'INSERT INTO Track (trackid, name, albumid, unitprice, mediatypeid, milliseconds) VALUES (?, ?, ?, ?, ?, ?)'
params = (3504, 'abc', 346, 1, 3, 325425)
sql_server.insert(query, params)
sql_server.close()
```
### Update
```python
sql_server.connect()
query = 'UPDATE Track SET milliseconds = ? WHERE trackid = ?'
params = (1234, 3504)
sql_server.update(query, params)
sql_server.close()
```

### Upsert
```python
sql_server.connect()
create_table_query = """
CREATE TABLE SampleTable (
    ID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Age INT
)
"""
upsert_query = """
MERGE INTO SampleTable AS target
USING (SELECT ? AS ID, ? AS Name, ? AS Age) AS source
ON target.ID = source.ID
WHEN MATCHED THEN 
    UPDATE SET Name = source.Name, Age = source.Age
WHEN NOT MATCHED THEN 
    INSERT (ID, Name, Age) VALUES (source.ID, source.Name, source.Age);
"""
data = [
    (1, 'Alice', 30),
    (2, 'Bob', 25),
    (3, 'Charlie', 28),
]
db.execute(create_table_query)
db.bulk_upsert(upsert_query, data)
sql_server.close()
```
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
>>> from db_setup_code import *

>>> def use_database(db: BaseDBInterface):

...     db.connect()

...     for row in db.read("SELECT * FROM Track"):

...         print(row)

...     db.close()

...

>>> sql_server = SQLServerDB(server='SK-INSPIRON-3K\MSSQLSERVER01', database='Chinook')

#This will print the table Track.

>>> use_database(sql_server)

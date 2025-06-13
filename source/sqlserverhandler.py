class SQLServerHandler:
    
    def __init__(self, server, database, driver='{ODBC Driver 17 for SQL Server}', username='', password=''):
        self.server = server
        self.database = database
        self.driver = driver
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish connection to SQL Server."""
        try:
            if self.username and self.password:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            else:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'

            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            print("Connected to SQL Server.")
        except Exception as e:
            print("Connection failed:", e)

    def read(self, query):
        """Run a SELECT query and return all results."""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def stream_read(self, query):
        """Run SELECT and yield results row-by-row."""
        self.cursor.execute(query)
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            yield row

    def insert(self, query, params):
        """Insert a single row using a parameterized query."""
        self.cursor.execute(query, params)
        #Writes changes to the database permanently
        self.conn.commit()

    def bulk_upsert(self, table, data):
        """
        Bulk upsert (insert or update) using MERGE. 
        Assumes each dict in `data` has the same keys (column names).
        """
        pass

    def update(self, query, params):
        """Run an UPDATE query with parameters."""
        self.cursor.execute(query, params)
        self.conn.commit()

    def execute(self, query):
        """Execute a raw SQL command (create, update, delete, drop, call procedure)."""
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        """Close DB connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection closed.")

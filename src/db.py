import mysql.connector

from config import DB_NAME, DB_PASSWORD

class DB: # A DB class for easier db connection management
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",      # server host
            user="root",           # My MySQL username
            password=DB_PASSWORD,  # database password
            database=DB_NAME
        )
        self.cursor = self.conn.cursor() # get the cursor

    def close(self):
        self.cursor.close()
        self.conn.close()



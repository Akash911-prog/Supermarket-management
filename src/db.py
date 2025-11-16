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
        """
        Close the database connection and cursor.

        This method is used to ensure the database connection and
        cursor are properly closed when the DB object is no longer
        needed.

        Returns:
            None
        """
        # Close the cursor
        self.cursor.close()

        # Close the connection
        self.conn.close()

    def add_item(self, name: str, description: str, price: float, stock: int):
        """
        Add an item to the database.

        Args:
            name (str): The name of the item.
            description (str): A description of the item.
            price (float): The price of the item.
            stock (int): The initial stock of the item.

        Returns:
            None
        """
        self.cursor.execute("INSERT INTO items (name, description, price, stock) VALUES (%s, %s, %s, %s)", (name, description, price, stock))
        self.conn.commit()

    def get_items(self):
        self.cursor.execute("SELECT * FROM items")
        return self.cursor.fetchall()

    def remove_item(self, item_id: int):
        self.cursor.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
        self.conn.commit()

    def update_item(self, item_id: int, field: str, value: str):
        self.cursor.execute(f"UPDATE items SET {field} = %s WHERE item_id = %s", (value, item_id))
        self.conn.commit()

    def create_order(self, total_price: float):
        self.cursor.execute("INSERT INTO orders (total_price) VALUES (%s)", (total_price,))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_order_items(self, order_items: dict):
        for items in order_items.values():
            self.cursor.execute("INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                                (items[0], items[1], items[4], items[3]))
            self.conn.commit()

    def get_daily_sales(self):
        self.cursor.execute("SELECT * FROM daily_sales")
        return self.cursor.fetchall()
    


    
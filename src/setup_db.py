from asyncio import exceptions
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from config import DB_NAME, TABLES, DB_PASSWORD

# ------------------------------------------
# Connect to MySQL Server
# ------------------------------------------
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",      # Change if needed
            user="root",           # Your MySQL username
            password=DB_PASSWORD  # <-- CHANGE THIS
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL server.")
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"❌ Connection Error: {err}")
        exit(1)

# ------------------------------------------
# Create Database
# ------------------------------------------
def create_database(cursor) -> None:
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"📦 Database `{DB_NAME}` is ready.")
    except mysql.connector.Error as err:
        print(f"❌ Database creation failed: {err}")
        exit(1)

# ------------------------------------------
# Create Tables
# ------------------------------------------
def create_tables(conn, cursor) -> None:
    try:
        cursor.execute(f"USE {DB_NAME}")
        for name, ddl in TABLES.items():
            cursor.execute(ddl)
            print(f"🧱 Table `{name}` created or already exists.")
        conn.commit()
    except mysql.connector.Error as err:
        print(f"❌ Table creation failed: {err}")
        exit(1)

# ------------------------------------------
# Insert Dummy Data
# ------------------------------------------
def insert_dummy_data(conn, cursor) -> None:
    items = [
        ("Maggie Noodles", "Instant noodles 70g pack", 15.00, 120),
        ("Colgate Toothpaste", "100g freshness gel", 55.00, 60),
        ("Dairy Milk", "Chocolate bar 40g", 45.00, 80),
        ("Amul Milk", "1L Tetra Pack", 68.00, 40),
        ("Parle G", "Biscuits pack 100g", 10.00, 200)
    ]

    cursor.executemany(
        "INSERT INTO items (name, description, price, stock) VALUES (%s, %s, %s, %s)",
        items
    )

    conn.commit()

    print(f"🍪 Inserted {cursor.rowcount} dummy products into `items`.")

def insert_dummy_orders(conn, cursor) -> None:
    """Insert dummy orders and their order items."""
    try:
        # Create 2 dummy orders
        orders = [
            (120.00,),  # total price
            (75.00,)
        ]
        cursor.executemany("INSERT INTO orders (total_price) VALUES (%s);", orders)
        conn.commit()

        # Get generated order IDs
        cursor.execute("SELECT order_id FROM orders;")
        order_ids = [row[0] for row in cursor.fetchall()]

        # Example order items (order_id, item_id, quantity)
        order_items = [
            (order_ids[0], 1, 2),  # 2 apples
            (order_ids[0], 2, 1),  # 1 milk
            (order_ids[1], 3, 3),  # 3 bread
        ]
        cursor.executemany("""
            INSERT INTO order_items (order_id, item_id, quantity)
            VALUES (%s, %s, %s);
        """, order_items)

        conn.commit()
        print("✅ Dummy orders and order items inserted!")

    except exceptions as e:
        print("❌ Error inserting dummy orders:", e)

# ------------------------------------------
# Main Setup Function
# ------------------------------------------
def main():
    conn, cursor = create_connection()
    create_database(cursor)
    create_tables(conn, cursor)
    cursor.execute(f"USE {DB_NAME}")

    # Check if dummy data already exists
    cursor.execute("SELECT COUNT(*) FROM items")
    (count,) = cursor.fetchone() #type: ignore
    if count == 0:
        insert_dummy_data(conn, cursor)
        insert_dummy_orders(conn, cursor)
    else:
        print("🟡 Dummy data already exists. Skipping insert.")

    cursor.close()
    conn.close()
    print("\n✅ Setup complete! Your database is ready to use.")

# ------------------------------------------
if __name__ == "__main__":
    main()
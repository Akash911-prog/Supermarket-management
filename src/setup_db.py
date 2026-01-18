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
            host="localhost",      # server host
            user="root",           # My MySQL username
            password=DB_PASSWORD    # database password
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
        cursor.execute("""CREATE VIEW daily_sales AS SELECT DATE(order_date) AS sale_date, SUM(total_price) AS total_sales FROM orders GROUP BY DATE(order_date);""")
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
        ("Parle G", "Biscuits pack 100g", 10.00, 200),
        ("Lays Chips", "Potato chips 50g pack", 20.00, 150),
        ("Nescafe Coffee", "Instant coffee 50g jar", 145.00, 35),
        ("Good Day Biscuits", "Cashew cookies 60g pack", 25.00, 110),
        ("Tata Salt", "Iodized salt 1kg pack", 22.00, 90),
        ("Red Label Tea", "Tea powder 250g pack", 95.00, 50),
        ("Fortune Oil", "Sunflower oil 1L bottle", 135.00, 45),
        ("Bournvita", "Health drink 75g pouch", 30.00, 70),
        ("Sprite", "Soft drink 750ml bottle", 40.00, 55),
        ("Dettol Soap", "Bathing soap 75g bar", 35.00, 85),
        ("Kellogg's Cornflakes", "Original 250g box", 115.00, 30)

    ]

    cursor.executemany(
        "INSERT INTO items (name, description, price, stock) VALUES (%s, %s, %s, %s)",
        items
    )

    conn.commit()

    print(f"🍪 Inserted {cursor.rowcount} dummy products into `items`.")

from datetime import date
import random

def insert_dummy_orders(conn, cursor):
    """Insert dummy orders for multiple dates with order items."""
    try:
        # ----------------------------
        # CONFIG
        # ----------------------------
        dates = [
        "2025-12-01",
        "2025-12-02",
        "2025-12-03",
        "2025-12-04",
        "2025-12-05",
        "2025-12-06",
        "2025-12-07",
        "2025-12-08",
        "2025-12-09",
        "2025-12-10",
        "2025-12-11",
        "2025-12-12",
        "2025-12-13",
        "2025-12-14",
        "2025-12-15",
        "2025-12-16",
        "2025-12-17",
        "2025-12-18",
        "2025-12-19",
        "2025-12-20",
        "2025-12-21",
        "2025-12-22",
        "2025-12-23",
        "2025-12-24",
        "2025-12-25",
        "2025-12-26",
        "2025-12-27",
        "2025-12-28",
        "2025-12-29",
        "2025-12-30",
        "2025-12-31",
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-05",
        "2026-01-06",
        "2026-01-07",
        "2026-01-08",
        "2026-01-09",
        ]
        # 5 dates → 5 * 5 = 25 orders

        orders_per_date = 5
        min_items_per_order = 1
        max_items_per_order = 4

        # ----------------------------
        # 1. Get item list for item_id + price
        # ----------------------------
        cursor.execute("SELECT item_id, price FROM items;")
        items = cursor.fetchall()  # (item_id, price)

        if not items:
            print("❌ No items found in `items` table.")
            return

        # ----------------------------
        # 2. Insert orders by date
        # ----------------------------
        all_order_ids = []

        for date in dates:
            order_records = [(random.uniform(50, 600), date) for _ in range(orders_per_date)]

            cursor.executemany(
                """
                INSERT INTO orders (total_price, order_date)
                VALUES (%s, %s);
                """,
                order_records
            )
            conn.commit()

            # Get back order_ids for this date only
            cursor.execute(
                "SELECT order_id FROM orders WHERE DATE(order_date) = %s ORDER BY order_id DESC LIMIT %s;",
                (date, orders_per_date)
            )
            fetched = [row[0] for row in cursor.fetchall()]
            all_order_ids.extend(fetched)

        # ----------------------------
        # 3. Insert order items
        # ----------------------------
        order_items_data = []

        for order_id in all_order_ids:
            num_items = random.randint(min_items_per_order, max_items_per_order)

            for _ in range(num_items):
                item_id, item_price = random.choice(items)
                quantity = random.randint(1, 5)

                order_items_data.append((order_id, item_id, quantity, item_price))

        cursor.executemany(
            """
            INSERT INTO order_items (order_id, item_id, quantity, price)
            VALUES (%s, %s, %s, %s);
            """,
            order_items_data
        )
        conn.commit()

        print(f"✅ Inserted {len(all_order_ids)} orders and {len(order_items_data)} order items successfully!")

    except Exception as e:
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
# ------------------------------------------
# Configuration
# ------------------------------------------

DB_NAME = "supermarket_db"

TABLES = {}

TABLES['items'] = (
    """
    CREATE TABLE IF NOT EXISTS items (
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(255),
        price DECIMAL(10,2) NOT NULL,
        stock INT NOT NULL DEFAULT 0
    );
    """
)

TABLES['orders'] = (
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_price DECIMAL(10,2)
    );
    """
)

TABLES['order_items'] = (
    """
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        item_id INT,
        quantity INT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES items(item_id)
    );
    """
)

TABLES['daily_sales'] = (
    """
    CREATE TABLE IF NOT EXISTS daily_sales (
        sale_id INT AUTO_INCREMENT PRIMARY KEY,
        sale_date DATE UNIQUE,
        total_sales DECIMAL(10,2)
    );
    """
)
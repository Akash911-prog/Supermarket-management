# ------------------------------------------
# Configuration
# ------------------------------------------
from InquirerPy.utils import get_style
from libs.helper import center_menu_block


DB_NAME = "supermarket_db"
DB_PASSWORD = "Mysql0914"
INDENT_RATIO = 0.4

TABLES = {}

base_choices = [
    ("add_item", "➕  Add Item"),
    ("view_inventory", "📦  View Inventory"),
    ("manage_inventory", "🛒  Manage Inventory"),
    ("view_sales", "📊  View Sales Report"),
    ("generate_bill", "🧾  Generate Bill"),
    ("exit", "🚪  Exit"),
]

base_manage_inv_choices = [
    ("add_item", "➕  Add Item"),
    ("remove_item", "❌  Remove Item"),
    ("update_item", "📝  Update Item"),
    ("exit", "🚪  Exit to Main Menu"),
]

base_bill_choices = [
    ("add", "➕  Add Item"),
    ("edit", "📝  Edit Bill"),
    ("current", "📃  Show Current Bill"),
    ("finalize", "✅  Finalize Bill"),
    ("cancel", "❌  Cancel"),
]

base_bill_edit_choices = [
    ("add", "➕  Add Item"),
    ("edit", "📝  Edit Bill"),
    ("current", "📃  Show Current Bill"),
    ("finalize", "✅  Finalize Bill"),
    ("cancel", "❌  Cancel"),
]

MAIN_MENU_CHOICES = center_menu_block(base_choices, indent_ratio=INDENT_RATIO)

MANAGE_INV_CHOICES = center_menu_block(base_manage_inv_choices, indent_ratio=0)

BILL_CHOICES = center_menu_block(base_bill_choices, indent_ratio=0)

MENU_STYLES = get_style({
    "questionmark": "#00C896 bold",
    "answer": "#90EE90 bold",
    "pointer": "#00C896 bold",
    "highlighted": "#00FFBF bold",
    "selected": "#00C896",
    "separator": "#808080",
    "instruction": "#C0C0C0 italic",
    "text": "#DCDCDC",
})

ITEM_FIELD_INDEX = {
    "item_id": 0,
    "name": 1,
    "description": 2,
    "price": 3,
    "stock": 4
}


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
        price Decimal(10,2) NOT NULL,
        total_price Decimal(10,2) AS (price * quantity) STORED,
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES items(item_id)
    );
    """
)


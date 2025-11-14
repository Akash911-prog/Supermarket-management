from add_item import add_item_main
from db import DB
from rich.table import Table
from rich.console import Console
from time import sleep
from InquirerPy import inquirer
from config import MENU_STYLES, MANAGE_INV_CHOICES
from libs.helper import center_text, clear_screen, show_menu_heading
from libs.fuzzy_search import fuzzy_search


def view_inventory():
    db = DB()
    console = Console()
    with console.status("[bold green]Loading inventory...[/bold green]"):
        items = db.get_items()
        sleep(1)
        
    table = Table(title="Inventory", title_style="bold cyan", border_style="#3C6382", style="#EAF0F1")
    table.add_column("Item ID", justify="right", style="bold blue")
    table.add_column("Item Name", justify="left", style="bold green")
    table.add_column("Description", justify="left", style="bold")
    table.add_column("Price", justify="right", style="bold cyan")
    table.add_column("Stock", justify="right", style="bold red")

    for item in items:
        table.add_row(str(item[0]), item[1], item[2], str(item[3]), str(item[4]))

    console.print(table)
    db.close()
    inquirer.confirm(message="Exit to main menu").execute()


def manage_inventory_menu():
    clear_screen()

    show_menu_heading("Manage Inventory")

    answer = inquirer.select(
        # Center the main menu text
        message=center_text("use arrow keys to navigate and enter to select"),
        # Use the predefined main menu choices
        choices=MANAGE_INV_CHOICES,
        # Use the predefined menu styles
        style=MENU_STYLES,
    ).execute()
    return answer

def manage_inventory():
    while True:
        choice = manage_inventory_menu()

        if choice == "add_item":
            add_item_main()
        elif choice == "remove_item" or choice == "update_item":
            item_id = fuzzy_search().id
            print(item_id)
        elif choice == "exit":
            break

if __name__ == "__main__":
    view_inventory()
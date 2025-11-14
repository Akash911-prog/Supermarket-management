from add_item import add_item_main
from db import DB
from rich.table import Table
from rich.console import Console
from time import sleep
from InquirerPy import inquirer
from config import MENU_STYLES, MANAGE_INV_CHOICES
from libs.helper import clear_screen, show_menu_heading, create_item_table
from libs.fuzzy_search import fuzzy_search
from remove_item import remove_item_main
from update_item import update_item_main


def view_inventory():
    db = DB()
    console = Console()
    with console.status("[bold green]Loading inventory...[/bold green]"):
        items = db.get_items()
        sleep(1)
        
    table = create_item_table()

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
        message="use arrow keys to navigate and enter to select",
        # Use the predefined main menu choices
        choices=MANAGE_INV_CHOICES,
        # Use the predefined menu styles
        style=MENU_STYLES,
    ).execute()
    return answer

def manage_inventory():
    while True:
        choice = manage_inventory_menu()
        console = Console()

        if choice == "add_item":
            add_item_main()
        elif choice == "remove_item" or choice == "update_item":
            item = fuzzy_search() # returns a tuple
            item_id = item[0] # returns the item id
            if choice == "remove_item":
                confirm = inquirer.confirm(message=f"Are you sure you want to remove {item[1]}?").execute()
                if not confirm:
                    continue
                remove_item_main(item_id)
                console.print(f"Item with Item Id: {item_id} has been removed successfully!", style="bold green on black")
                sleep(0.5)
            elif choice == "update_item":
                updated_fields = update_item_main(item_id)
                console.print(f"Item with Item Id: {item_id} has been updated successfully!", style="bold green on black")
                sleep(0.5)
            input("Press enter to continue...")
        elif choice == "exit":
            break

if __name__ == "__main__":
    view_inventory()
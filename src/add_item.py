from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
from rich.traceback import install
from rich.panel import Panel
from rich.table import Table
from time import sleep
from libs.helper import clear_screen, show_menu_heading
from config import MENU_STYLES
from db import DB

install() # formats the error messages if any
console = Console() # the console object used in rich to format text

items_to_add = []

def add_item_to_db(items_to_add):
    db = DB()
    for i in items_to_add:
        db.add_item(i[0], i[1], i[2], i[3])

    db.close()

def add_item_menu():

    clear_screen()

    show_menu_heading("Add Items")

    name = inquirer.text(
        message="Enter the name of the item: ").execute()

    if name == '':
        return

    description = inquirer.text(
        message="Enter a description for the item: ", 
        validate=EmptyInputValidator()).execute()
    price = inquirer.number(
        message="Enter the price of the item: ", 
        float_allowed=True, validate=lambda x: float(x) > 0, 
        filter=lambda x: float(x), 
        invalid_message="price needs to be greater than 0").execute()
    stock = inquirer.number(
        message="Enter the initial stock of the item: ", 
        float_allowed=False, validate=lambda x: int(x) > 0, 
        filter=lambda x: int(x), 
        invalid_message="stock needs to be greater than 0").execute()
    
    items_to_add.append((name, description, price, stock))
    

    console.print("Item added successfully!", style="bold green on black")
    sleep(1)


def print_to_add_items():

    table = Table(show_lines=True, title="Items added", title_style="bold cyan on black", border_style="#3C6382", style="#EAF0F1")
    table.add_column("Name", justify="left", style="bold ")
    table.add_column("Description", justify="left", style="bold")
    table.add_column("Price", justify="left", style="bold")
    table.add_column("Stock", justify="left", style="bold")

    for item in items_to_add:
        table.add_row(item[0], item[1], str(item[2]), str(item[3]))

    console.print(table)


def add_item_main():
    while True:
        add_item_menu()
        confirm = inquirer.confirm(
            message="Do you want to add another item?",
            default=True,
            style=MENU_STYLES,
        ).execute()

        if not confirm:
            if len(items_to_add) > 0:
                print_to_add_items()
                add_item_to_db(items_to_add)
                input("Press enter to continue...")
            break


if __name__ == "__main__":

    add_item_main()

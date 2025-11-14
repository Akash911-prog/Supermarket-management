from pydoc import text
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
from rich.traceback import install
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from time import sleep
from libs.helper import clear_screen
from config import MENU_STYLES
from db import DB

install() # formats the error messages if any
console = Console() # the console object used in rich to format text
db = DB()

items_to_add = []

def add_item_to_db(items_to_add):
    for i in items_to_add:
        db.add_item(i[0], i[1], i[2], i[3])

def add_item_menu():

    clear_screen()
    text = Align.center(
        "Add Item",
        style="bold cyan on black",)
    
    console.print(Panel(text, width=60, style="bold cyan on black"))

    name = inquirer.text(message="Enter the name of the item: ", validate=EmptyInputValidator()).execute()
    description = inquirer.text(message="Enter a description for the item: ", validate=EmptyInputValidator()).execute()
    price = inquirer.number(message="Enter the price of the item: ", float_allowed=True, validate=EmptyInputValidator()).execute()
    stock = inquirer.number(message="Enter the initial stock of the item: ", float_allowed=False, validate=EmptyInputValidator()).execute()

    if ( 
        float(price) <= 0
        or int(stock) <= 0
        ):
        console.print("❌ Invalid input. Please try again.", style="bold red on black")
        sleep(1)
        return
    
    items_to_add.append((name, description, price, stock))
    

    console.print("Item added successfully!", style="bold green on black")
    sleep(1)


def print_to_add_items():
    table = Panel.fit(
        "[b][/b]",
        title="Items to add",
        title_align="center",
        style="bold cyan on black",
    )


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
                add_item_to_db(items_to_add)
            break


if __name__ == "__main__":

    add_item_main()

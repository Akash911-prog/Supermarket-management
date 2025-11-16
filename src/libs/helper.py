import shutil
from InquirerPy.base.control import Choice
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.table import Table
import os

console = Console() # used for print formating in rich library

def center_text(text: str) -> str:
    """Return text roughly centered in terminal width."""
    width = shutil.get_terminal_size().columns
    padding = max((width - len(text)) // 2, 0)
    return " " * padding + text

def clear_screen():
    """
    Clears the terminal screen using the appropriate command for the operating system.

    If the operating system is Windows (os.name == 'nt'), the function uses the 'cls' command.
    Otherwise, it uses the 'clear' command.

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def exit_program():
    """
    Exits the program after clearing the screen and printing a goodbye message.

    Clears the terminal screen, prints "Goodbye!" in bold green, waits for 1 second, and then exits the program.

    Returns:
        None
    """
    clear_screen()
    console.print("Goodbye!", style="bold green")
    exit()



def center_menu_block(choices, indent_ratio=0.25):
    """Add equal left margin to all choices to center menu block visually."""
    width = shutil.get_terminal_size().columns
    indent = int(width * indent_ratio)
    prefix = " " * indent
    return [Choice(value=c[0], name=prefix + c[1]) for c in choices]



def show_menu_heading(text):
    """
    Prints a centered menu heading with a border below.

    Args:
        text (str): The text to display as the menu heading.

    Prints a centered menu heading with a border below using the rich library.
    The menu heading is displayed in bold cyan on black style.
    The border below the menu heading is displayed in bold cyan on black style.
    """
    text = Align.center(
        f"{text} \n{'-'*len(text)}",
        style="bold cyan on black",)
    
    console.print(Panel(text, width=60, style="bold cyan on black"))

def create_item_table():
    """
    Creates a table to display the items in the inventory.

    The table has 5 columns: Item ID, Item Name, Description, Price, and Stock.
    The columns are justified and styled using the rich library.

    Returns:
        Table: A rich table object to display the items in the inventory.
    """
    table = Table(title="Inventory", title_style="bold cyan", border_style="#3C6382", style="#EAF0F1")
    table.add_column("Item ID", justify="right", style="bold blue")
    table.add_column("Item Name", justify="left", style="bold green")
    table.add_column("Description", justify="left", style="bold")
    table.add_column("Price", justify="right", style="bold cyan")
    table.add_column("Stock", justify="right", style="bold red")
    return table

def create_bill_table():
    """
    Creates a table to display the items in the bill.

    The table has 5 columns: Item ID, Item Name, Price, Quantity, and Total.
    The columns are justified and styled using the rich library.

    Returns:
        Table: A rich table object to display the items in the bill.
    """
    table = Table(show_lines=True, title="Current Bill", title_style="bold cyan on black", border_style="#3C6382", style="#EAF0F1")
    # Add columns to the table
    table.add_column("Item ID", justify="right", style="bold blue")
    table.add_column("Item Name", justify="left", style="bold green")
    table.add_column("Price", justify="left", style="bold cyan")
    table.add_column("Quantity", justify="left", style="bold red")
    table.add_column("Total", justify="left", style="bold green")

    return table
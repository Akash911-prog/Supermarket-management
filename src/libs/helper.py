import shutil
from InquirerPy.base.control import Choice
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.table import Table
import os
from time import sleep

console = Console()

def center_text(text: str) -> str:
    """Return text roughly centered in terminal width."""
    width = shutil.get_terminal_size().columns
    padding = max((width - len(text)) // 2, 0)
    return " " * padding + text

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def exit_program():
    clear_screen()
    print("Goodbye!")
    sleep(1)
    exit()



def center_menu_block(choices, indent_ratio=0.25):
    """Add equal left margin to all choices to center menu block visually."""
    width = shutil.get_terminal_size().columns
    indent = int(width * indent_ratio)
    prefix = " " * indent
    return [Choice(value=c[0], name=prefix + c[1]) for c in choices]



def show_menu_heading(text):

    text = Align.center(
        f"{text} \n{'-'*len(text)}",
        style="bold cyan on black",)
    
    console.print(Panel(text, width=60, style="bold cyan on black"))

def create_item_table():
    table = Table(title="Inventory", title_style="bold cyan", border_style="#3C6382", style="#EAF0F1")
    table.add_column("Item ID", justify="right", style="bold blue")
    table.add_column("Item Name", justify="left", style="bold green")
    table.add_column("Description", justify="left", style="bold")
    table.add_column("Price", justify="right", style="bold cyan")
    table.add_column("Stock", justify="right", style="bold red")
    return table
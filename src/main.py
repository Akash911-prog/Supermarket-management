from InquirerPy import inquirer
from rich.console import Console
from rich.traceback import install
from rich.align import Align
from rich.panel import Panel
from pyfiglet import Figlet
import os
from time import sleep
from libs.helper import center_text
from config import MENU_STYLES, MAIN_MENU_CHOICES

install()
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_centered_title(title):
    f = Figlet(font="slant", width=320)
    text = f.renderText(title)
    console.print(Align.center(Panel(f"[bold cyan]{text}[/bold cyan]")))

def create_main_menu():
    answer = inquirer.select(
        message=center_text("Main Menu"),
        choices=MAIN_MENU_CHOICES,
        style=MENU_STYLES,
    ).execute()
    return answer

def main():
    clear_screen()
    show_centered_title("Supermarket Management System ")
    choice = create_main_menu()
    clear_screen()
    print(f"You selected: {choice}")
    sleep(1)

if __name__ == "__main__":
    main()

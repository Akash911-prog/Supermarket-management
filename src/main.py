from InquirerPy import inquirer
from rich.console import Console
from rich.traceback import install
from time import sleep
from libs.helper import center_text, clear_screen
from libs.map_choices import map_choices
from config import MENU_STYLES, MAIN_MENU_CHOICES

install() # formats the error messages if any
console = Console() # the console object used in rich to format text


def show_centered_title(title):
    console.print(title, style="bold cyan on black", justify="center")
    console.print("-" * len(title), style="bold cyan on black", justify="center")

def create_main_menu():
    """
    Create the main menu using InquirerPy's select module.

    Returns:
        str: The selected menu option
    """

    show_centered_title("Main Menu")

    answer = inquirer.select(
        # Center the main menu text
        message=center_text("use arrow keys to navigate and enter to select"),
        # Use the predefined main menu choices
        choices=MAIN_MENU_CHOICES,
        # Use the predefined menu styles
        style=MENU_STYLES,
    ).execute()
    return answer

def main():
    """
    The main function that runs the program.

    This function creates a loop that displays the main menu, gets the user's choice,
    and maps the choice to the corresponding function.

    Returns:
        None
    """
    while True:
        # Clear the screen
        clear_screen()
        # Show the title
        show_centered_title("Supermarket Management System ")
        # Create the main menu
        choice = create_main_menu()
        # Clear the screen
        clear_screen()
        # Map the choice to the corresponding function
        map_choices(choice)

        sleep(0.1)

if __name__ == "__main__":
    main()

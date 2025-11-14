from db import DB
from InquirerPy import inquirer

from libs.fuzzy_search import fuzzy_search
from libs.helper import clear_screen, show_menu_heading
from config import MENU_STYLES, BILL_CHOICES, ITEM_FIELD_INDEX


items_cache : dict[str, list] = {}

def show_billing_menu():
    show_menu_heading("Billing")

    answer = inquirer.select(
        # Center the main menu text
        message="use arrow keys to navigate and enter to select",
        # Use the predefined main menu choices
        choices=BILL_CHOICES,
        # Use the predefined menu styles
        style=MENU_STYLES,
    ).execute()
    return answer

def billing_choice_map(choice):
    options = {
    "add": add_item_to_bill,
    "edit": "📝  Edit Bill",
    "remove": "❌  Remove Item",
    "current": "📃  Show Current Bill",
    "finalize": "✅  Finalize Bill",
    "cancel": "❌  Cancel"
    }

    return options[choice]

def show_current_bill():
    pass

def finalize_bill():
    pass

def edit_bill():
    pass

def add_item_to_bill():
    while True:
        item = fuzzy_search('Choose the item you want to add: ')
        quantity = inquirer.number(message="Enter the quantity: ", transformer=lambda x: int(x), validate=lambda x: int(x) > 0).execute()
        items_cache[item[1]] = [0, item[ITEM_FIELD_INDEX["item_id"]], item[ITEM_FIELD_INDEX["name"]], item[ITEM_FIELD_INDEX["price"]], quantity]

        confirm = inquirer.confirm(message="Do you want to add another item?", default=True).execute()
        if not confirm:
            break

def show_edit_bill_menu():
    pass

def bill_main():
    pass
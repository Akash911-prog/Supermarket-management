
from add_item import add_item_main
from libs.helper import exit_program

def map_choices(choice):
    options = {
        "add_item": add_item_main,
        "view_inventory": "view_inventory",
        "view_sales": "view_sales",
        "generate_bill": "generate_bill",
        "exit": exit_program,
    }

    options[choice]()
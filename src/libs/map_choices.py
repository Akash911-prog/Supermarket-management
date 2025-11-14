
from add_item import add_item_main
from libs.helper import exit_program
from libs.fuzzy_search import fuzzy_search
from inventory import view_inventory, manage_inventory

def map_choices(choice):
    options = {
        "add_item": add_item_main,
        "view_inventory": view_inventory,
        "manage_inventory": manage_inventory,
        "view_sales": fuzzy_search,
        "generate_bill": "generate_bill",
        "exit": exit_program,
    }

    options[choice]()



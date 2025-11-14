
from add_item import add_item_main
from libs.helper import exit_program
from sales_report import sales_report_main
from inventory import view_inventory, manage_inventory
from billing import bill_main

def map_choices(choice):
    options = {
        "add_item": add_item_main,
        "view_inventory": view_inventory,
        "manage_inventory": manage_inventory,
        "view_sales": sales_report_main,
        "generate_bill": bill_main,
        "exit": exit_program,
    }

    options[choice]()



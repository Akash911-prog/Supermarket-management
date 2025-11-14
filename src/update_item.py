from db import DB
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
from config import MENU_STYLES
from libs.helper import clear_screen, show_menu_heading


def get_updation_fields():

    fields_to_update = {}

    while True:
        field = inquirer.select(
            message="Select a field to update:",
            choices=[
                "name",
                "description",
                "price",
                "stock",
            ],
        ).execute()


        if field == "price":
            value = inquirer.number(
                message=f"Enter the new value for {field}: ",
                float_allowed=True,
                validate=lambda x: float(x) > 0,
                transformer=lambda x: float(x),
                invalid_message="price needs to be greater than 0",
            ).execute()

        elif field == "stock":
            value = inquirer.number(
                message=f"Enter the new value for {field}: ",
                float_allowed=False,
                validate=lambda x: int(x) > 0,
                transformer=lambda x: int(x),
                invalid_message="stock needs to be greater than 0",
            ).execute()
        
        else:
            value = inquirer.text(
                message=f"Enter the new value for {field}: ",
                validate=EmptyInputValidator(),
            ).execute()

        fields_to_update[field] = value

        confirm = inquirer.confirm(
            message="Do you want to update another field?",
            default=True,
            style=MENU_STYLES,
        ).execute()

        if not confirm:
            break

    return fields_to_update


def update_item_main(item_id: int):
    db = DB()
    console = Console()
    clear_screen()
    show_menu_heading("Update Item")

    fields_to_update = get_updation_fields()

    for field, value in fields_to_update.items():
        db.update_item(item_id, field, value)

    console.print("Item updated successfully!", style="bold green on black")
    db.close()
    return fields_to_update
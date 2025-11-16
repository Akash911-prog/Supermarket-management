from db import DB
from InquirerPy import inquirer
from rich.console import Console
from libs.fuzzy_search import fuzzy_search
from libs.helper import clear_screen, show_menu_heading, create_bill_table
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
    """
    A function to map the user's choice to the corresponding function.

    This function takes the user's choice and maps it to the corresponding function.
    If the user chooses to view the current bill, the function will call the
    show_current_bill function and then wait for the user to press enter.
    Otherwise, the function will call the corresponding function without waiting.

    Args:
        choice (str): The user's choice.

    Returns:
        None
    """

    options = {
        # Add an item to the bill
        "add": add_item_to_bill,
        # Edit the bill
        "edit": edit_bill,
        # Show the current bill
        "current": show_current_bill,
        # Finalize the bill
        "finalize": finalize_bill,
        # Cancel the bill
        "cancel": 'cancel'
    }

    if choice == "current":
        options[choice]()
        input("Enter to continue...")
    else:
        options[choice]()



def show_current_bill():
    """
    A function to show the current bill.

    This function will clear the screen, create a table to display the items in the bill,
    and then print the table to the console.

    If there are no items in the bill, the function will print a message to the user.
    """
    clear_screen()
    console = Console()

    if len(items_cache) == 0:
        console.print("No items in the bill.", style="bold red")
        return

    table = create_bill_table()

    # Add rows to the table from the items_cache dictionary
    for item in items_cache.values():
        table.add_row(str(item[1]), item[2], str(item[3]), str(item[4]), str(item[3] * item[4])) # item id, name, price, quantity, total
    # If there are no items in the bill, print a message to the user
    # Print the table to the console
    console.print(table)

def finalize_bill():
    db = DB()
    total_price = 0
    for i in items_cache.values():
        total_price += i[3] * i[4]
    order_id = db.create_order(total_price)
    for i in items_cache.values():
        i[0] = order_id
    
    db.add_order_items(items_cache)
    db.close()

    table = create_bill_table()
    for item in items_cache.values():
        table.add_row(str(item[1]), item[2], str(item[3]), str(item[4]), str(item[3] * item[4]))

    console = Console()
    console.print(table)
    console.print(f"Total price: {total_price}", style="bold green")
    console.print()
    console.print("Bill finalized successfully!", style="bold green on black")
    input("Press enter to continue...")
    return True



def edit_bill():
    """
    A function to edit the bill.

    This function will first show the current bill using show_current_bill.
    Then, it will ask the user to choose an item to edit.
    If the user chooses to change the quantity, they will be asked to enter the new quantity.
    The quantity of the item will then be updated in the items_cache dictionary.
    If the user chooses to remove the item, the item will be removed from the items_cache dictionary.
    The function will then show the updated bill using show_current_bill.
    Finally, the function will ask the user if they want to edit another item.
    If the user chooses not to edit another item, the function will break out of the loop.
    """
    while True:
        console = Console()
        show_current_bill()
        item = inquirer.fuzzy(message="Choose the item you want to edit: ", choices=list(items_cache.keys())).execute()
        choice = inquirer.select(message="What do you want to do?", choices=["change_quantity", "remove_item"]).execute()

        if choice == "change_quantity":
            # Ask the user to enter the new quantity
            quantity = inquirer.number(message="Enter the quantity: ", filter=lambda x: int(x),
                                       validate=lambda x: int(x) > 0,
                                       default=int(items_cache[item][4])).execute()
            # Update the quantity of the item in the items_cache dictionary
            items_cache[item][4] = quantity
            # Show the updated bill
            show_current_bill()
            # Print a message to the user
            console.print(f"Quantity of {item} has been changed to {quantity}", style="bold green on black")
        elif choice == "remove_item":
            # Remove the item from the items_cache dictionary
            del items_cache[item]
            # Show the updated bill
            show_current_bill()
            # Print a message to the user
            console.print(f"Item {item} has been removed from the bill", style="bold green on black")

        # Ask the user if they want to edit another item
        choice = inquirer.confirm(message="Do you want to edit another item?", default=True).execute()
        if not choice:
            break

def add_item_to_bill():
    """
    A function to add items to the bill.

    This function will first search for the item to add using fuzzy_search,
    then prompt the user to enter the quantity of the item they want to add.
    The item and its quantity will then be added to the items_cache dictionary.
    The function will then show the current bill using show_current_bill.
    Finally, the function will ask the user if they want to add another item.
    If the user chooses not to add another item, the function will break out of the loop.
    """
    while True:
        item = fuzzy_search('Choose the item you want to add: ')
        quantity = inquirer.number(message="Enter the quantity: ",
                                   filter=lambda x: int(x), 
                                   validate=lambda x: int(x) > 0).execute()
        items_cache[item[1]] = [
            0,
            item[ITEM_FIELD_INDEX["item_id"]],
            item[ITEM_FIELD_INDEX["name"]],
            item[ITEM_FIELD_INDEX["price"]],
            quantity
            ]

        show_current_bill()

        # console.log(type(item[ITEM_FIELD_INDEX["price"]]), type(quantity))
        confirm = inquirer.confirm(message="Do you want to add another item?", default=True).execute()
        if not confirm:
            break

def show_edit_bill_menu():
    pass

def bill_main():
    while True:
        global items_cache
        clear_screen()
        choice = show_billing_menu()
        if choice == "cancel":
            items_cache.clear()
            break
        billing_choice_map(choice)
        if choice == "finalize":
            items_cache.clear()
            break

if __name__ == "__main__":

    bill_main()
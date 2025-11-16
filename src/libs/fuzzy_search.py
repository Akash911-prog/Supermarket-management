from InquirerPy import inquirer
from db import DB


def fuzzy_search(text="Search for an item: ") -> tuple[int, str, str, float, int] | str:
    db = DB()
    items_raw = db.get_items()
    items = {item[1]: item for item in items_raw}
    item_names = list(items.keys())

    item_name = inquirer.fuzzy(message=text, choices=["Cancel"] + item_names).execute()
    if item_name == "Cancel": 
        return "Cancel"
    item = items[item_name]
    db.close()
    return item





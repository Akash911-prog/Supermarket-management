from InquirerPy import inquirer
from db import DB


def fuzzy_search() -> tuple[int, str, str, float, int]:
    db = DB()
    items_raw = db.get_items()
    items = {item[1]: item for item in items_raw}
    item_names = list(items.keys())

    item_name = inquirer.fuzzy(message="Search for an item: ", choices=item_names).execute()
    item = items[item_name]
    db.close()
    return item
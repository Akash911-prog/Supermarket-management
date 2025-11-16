from db import DB

def remove_item_main(item_id: int):
    db = DB()
    db.remove_item(item_id)
    db.close()




    
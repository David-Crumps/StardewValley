import sqlite3
from database_manager import DatabaseManager

class CropItem:
    #Constructor: calls database manager passing crop_item_id, generates a CropItem from the value in the database with the id used in the calling
    def __init__(self, crop_item_id):
        db = DatabaseManager()
        crop_data = db.fetch_one("SELECT * FROM CropItems WHERE crop_item_id=?", (crop_item_id,))

        if crop_data:
            self.crop_item_id, self.name, self.crop_sell_price = crop_data
        else:
            raise ValueError("Crop item not found!")

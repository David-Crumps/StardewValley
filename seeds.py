import sqlite3
from database_manager import DatabaseManager

class Seed:
    #Constructor: calls database with value of seed_id and generates instance.
    def __init__(self, seed_id):
        db = DatabaseManager()
        seed_data = db.fetch_one("SELECT * FROM Seeds WHERE seed_id=?", (seed_id,))

        if seed_data:
            self.seed_id, self.name, self.cost, self.sell_price, self.plant_id = seed_data
        else:
            raise ValueError("Seed not found!")
    #Class method: Returns all seed names found in the table Seeds
    @classmethod
    def getSeedNames(cls):
        db = DatabaseManager()
        seed_names = db.fetch_all("SELECT name FROM Seeds")
        return_seeds = [row[0] for row in seed_names]
        return return_seeds
    
    #Class method: Takes in the seed name and returns the appropriate id from the db.
    @classmethod
    def getSeedIDFromName(cls, name):
        db = DatabaseManager()
        seed_id = db.fetch_one("SELECT seed_id FROM Seeds WHERE name=?", (name,))
        return seed_id[0]

  

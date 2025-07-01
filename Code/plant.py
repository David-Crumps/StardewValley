import sqlite3
from database_manager import DatabaseManager
from constants import SEASON_ORDER

class Plant:
    #Constructor: calls database manager passing plant_id, generates a Plant item from the item in the database with the same id.
    def __init__(self, plant_id):
        db = DatabaseManager()
        plant_data = db.fetch_one("SELECT * FROM Plants WHERE plant_id=?", (plant_id,))

        if plant_data:
            self.plant_id, self.name, self.grow_time, self.regrowth_time, self.crops_per_harvest, self.crop_item_id = plant_data

            #Get all season names from the season table, by joining via the plantSeasons Table
            season_results = db.fetch_all("""
                    SELECT s.name FROM Seasons s
                    JOIN PlantSeasons ps on s.season_id = ps.season_id
                    WHERE ps.plant_id =?""", (plant_id,))
            self.grow_seasons = [row[0] for  row in season_results]
            self.grow_seasons.sort(key=lambda s: SEASON_ORDER[s])
        else:
            raise ValueError("Plant not found!")

import numpy as np
from database_manager import DatabaseManager
from seeds import Seed
from plant import Plant
from cropitem import CropItem
from constants import *
import json

class CropController:
    def __init__(self, seed_id):
        self.seed = Seed(seed_id)
        self.plant = Plant(self.seed.plant_id)
        self.crop_item = CropItem(self.plant.crop_item_id)

    def getTableInformation(self):
        return [self.crop_item.name, self.plant.grow_seasons, self.seed.cost, self.crop_item.crop_sell_price,
                self.plant.grow_time, self.plant.regrowth_time]

    #Class method: takes in a season name and return all
    #seed names associated with that season in the database (move to db manager class?)
    @classmethod
    def getSeedNameFromSeason(cls, seasonName):
        db = DatabaseManager()
        names = db.fetch_all("""SELECT s.name from Seeds s
                        JOIN Plants p on s.plant_id = p.plant_id
                        JOIN PlantSeasons ps on p.plant_id = ps.plant_id
                        JOIN Seasons x on ps.season_id = x.season_id
                        WHERE x.name=?""", (seasonName,))
        return [row[0] for row in names]


    #Return a dictionary of seasons, and the amount of harvests in that seasons
    def regrowableHarvest(self, seasonPlanted, dayPlanted, fertiliser):
        #List of seasons in which the plant will grow in, given which season the inital planting occurs.
        actualSeasons = getSeasonRange(seasonPlanted, self.plant.grow_seasons[-1])
        seasonHarvest = []
        #Initalise seasonHarvest.
        for i in range(len(actualSeasons)):
            seasonHarvest.append(0)
        fertiliser_value = getSpeedFertiliserValue(fertiliser)
        initial_grow = int(self.plant.grow_time*(1-fertiliser_value))
        del fertiliser_value

        days = 0
        remainder_days = 0
        total = 0
        harvestDict = {}
        for i in range(len(actualSeasons)):
            #If there are leftover days from the previous season, subtract them from the current season
            if (remainder_days > 0):
                days = DAYS_IN_SEASON-remainder_days
            else:
                #otherwise subtract dayPlanted and growTime from the current season amount of days (28)
                days = DAYS_IN_SEASON - dayPlanted - initial_grow 

            if (days < 0):
                #If days is less than 0 growing goes into the next season, set remainder to the excess
                remainder_days = abs(days) 
            else:
                #If the plant regrows
                if self.plant.regrowth_time > 0:
                    real_num_harvests = days/self.plant.regrowth_time
                    remainder_days = (self.plant.regrowth_time*(1-(real_num_harvests%1))) #redundant for some regrowing plants (blueberry etc), but is required for multiseason crops
                else:
                    #If the plant doesn't regrow, but is selected to be replanted
                    real_num_harvests = days/initial_grow
                    
                seasonHarvest[i] += 1+(int(real_num_harvests))
                harvestDict[actualSeasons[i]] = seasonHarvest[i]
                total += seasonHarvest[i]
                
        harvestDict["Total"] = total   
        return(harvestDict)

    def singleHarvest(self, seasonPlanted, dayPlanted):
        actualSeasons = getSeasonRange(seasonPlanted, self.plant.grow_seasons[-1])
        harvestDay = DAYS_IN_SEASON - dayPlanted - self.plant.grow_time
        
        harvestDict = {}
        if (harvestDay >= 0):
            harvestDict[actualSeasons[0]] = 1
        else:
            if (len(actualSeasons) > 1):
                harvestDict[actualSeasons[1]] = 1
        return harvestDict

    def determineQualityOfHarvest(self, farmingLevel, fertilizer, amountOfCrops):
        fertilizerVal = getQualityFertiliserValue(fertilizer)
        if fertilizerVal == 3:
            return self.determineIridiumQualityOfHarvest(farmingLevel, fertilizerVal, amountOfCrops)
        else:
            gold_chance = calculateGoldChance(farmingLevel, fertilizerVal)
            num_gold = int(np.sum(np.random.rand(amountOfCrops) < gold_chance))

            remaining = amountOfCrops - num_gold
            silver_chance = calculateSilverChance(gold_chance)
            num_silver = int(np.sum(np.random.rand(remaining) < silver_chance))

            num_regular = remaining - num_silver
            num_regular += int((self.plant.crops_per_harvest-1)*amountOfCrops)
            return{"Regular": num_regular, "Silver": num_silver, "Gold": num_gold}

    def determineIridiumQualityOfHarvest(self, farmingLevel, fertilizerVal, amountOfCrops):
        gold_chance = calculateGoldChance(farmingLevel, fertilizerVal)

        iridium_chance = calculateIridiumChance(gold_chance)

        num_iridium = int(np.sum(np.random.rand(amountOfCrops) < iridium_chance))

        remaining = amountOfCrops - num_iridium

        num_gold = int(np.sum(np.random.rand(remaining) < gold_chance))
        num_silver = remaining - num_gold

        num_regular = int((self.plant.crops_per_harvest-1)*amountOfCrops)
        return{"Regular": num_regular, "Silver": num_silver, "Gold": num_gold, "Iridium": num_iridium}

    #Return a dictionary of profits based on each quality type for a given crop
    def determineEstimatedProfit(self, qualityDict, numHarvests):
        return sum(qualityDict[quality]*int(QUALITY_MULTIPLIERS[quality]*self.crop_item.crop_sell_price)*numHarvests for quality in qualityDict if quality in QUALITY_MULTIPLIERS)

    def determineCost(self, amountPurchased):
        return amountPurchased*self.seed.cost
        
        
        
        

        
                
            
        

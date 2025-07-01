SEASON_ORDER = {
    "Spring": 1,
    "Summer": 2,
    "Fall": 3,
    "Winter": 4
}
DAYS_IN_SEASON = 28
SEASONS = ["Spring", "Summer", "Fall", "Winter"]

SPEED_FERTILISERS = {
    "Speed-Gro": 0.1,
    "Deluxe Speed-Gro": 0.25,
    "Hyper Speed-Gro": 0.33
}
QUALITY_FERTILISERS = {"Basic Fertilizer": 1, "Quality Fertilizer": 2, "Deluxe Fertilizer": 3}

QUALITY_MULTIPLIERS = {"Regular": 1, "Silver": 1.25, "Gold": 1.5, "Iridium": 2} 

#Return an ordered list of all seasons this are between a start season and end season (inclusive)
def getSeasonRange(start_season, end_season):
    start_index = SEASON_ORDER[start_season]
    end_index = SEASON_ORDER[end_season]

    season_range = [season for season, index in SEASON_ORDER.items() if start_index <= index <= end_index]
    
    return season_range

def getSpeedFertiliserValue(name):
    
    if name in SPEED_FERTILISERS:
        value = SPEED_FERTILISERS[name]
        return value
    else:
        return 0

def getQualityFertiliserValue(name):
    if name in QUALITY_FERTILISERS:
        value = QUALITY_FERTILISERS[name]
        return value
    else:
        return 0

def calculateGoldChance(farmingLevel, fertilizer):
    return round((0.2*(farmingLevel/10)) + (0.2*fertilizer)*((farmingLevel+2)/12) + 0.01, 2)

def calculateSilverChance(gold_chance):
    return round(min(0.75, 2*gold_chance), 2)

def calculateIridiumChance(gold_chance):
    return round(gold_chance/2, 2)



    










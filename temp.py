import random
import numpy as np



xd = ["abc", "cbd"]

def qualityFormula(farmingLevel, fertilizer):
    qualityDict = {}
    qualityDict["Gold"] = round((0.2*(farmingLevel/10))+(0.2*(fertilizer)*((farmingLevel+2)/12))+0.01, 2)
    qualityDict["Silver"] = round((1-qualityDict["Gold"])*(min(0.75, qualityDict["Gold"]*2)), 2)
    qualityDict["Regular"] = round(1-qualityDict["Gold"]-qualityDict["Silver"], 2)
    print(qualityDict)
                                                     
#Looping is bad
def determineFarmingQuality(farmingLevel, fertilizer, amount):
    gold_chance = round((0.2*(farmingLevel/10))+(0.2*(fertilizer)*((farmingLevel+2)/12))+0.01, 2)
    silver_chance = round(min(0.75, 2*gold_chance), 2)
    dictCrops = {"Regular": 0, "Silver": 0, "Gold": 0}
    for _ in range(amount):
        if (random.random() < gold_chance):
            dictCrops["Gold"] += 1
        elif (random.random() < silver_chance):
            dictCrops["Silver"] += 1
        else:
            dictCrops["Regular"] += 1
    print(dictCrops)

#determineFarmingQuality(14,2,100)



#This is the one, it doesn't loop, just generates amount number of values between 0 and 1, then does the same on the remaining amounts for silver chance
def determineFarmingQualityTwo(farmingLevel, fertilizer, amount):
    #In-game forumla to determine gold crop
    gold_chance = round((0.2*(farmingLevel/10)) + (0.2*fertilizer)*((farmingLevel+2)/12) + 0.01, 2)
    
    #Create an array of values between 0 (inclusive) and 1 (exclusive) of length amount, and tally up all values less than gold_chance
    num_gold = int(np.sum(np.random.rand(amount) < gold_chance))
    
    #Figure out how many crops are left after removing the number of gold
    remaining = amount - num_gold
    
    #In game formula to determine silver crop
    silver_chance = round(min(0.75, 2*gold_chance), 2)
    
    #Same as num_gold, but using silver_chance and the remaning crops not the total.
    num_silver = int(np.sum(np.random.rand(remaining) < silver_chance))
    num_regular = remaining - num_silver
    return {"Regular": num_regular, "Silver": num_silver, "Gold": num_gold}
#These amounts should then be multiplied by the amount of harvests and then sent for profitaking, i.e multiplying by respective sell prices (per quality) and then mutliplying (crops_per_harvests-1)*base_sell_price*harvests




print(determineFarmingQualityTwo(14,2,1))

def determineIridiumQuality(farmingLevel, fertilizer, amount):
    initial_gold_chance = round((0.2*(farmingLevel/10)) + (0.2*fertilizer)*((farmingLevel+2)/12) + 0.01, 2)
    print(initial_gold_chance)
    iridium_chance = round(initial_gold_chance/2, 2)
    print(iridium_chance)
    actual_gold_chance = round((1-iridium_chance)*initial_gold_chance, 2)
    print(actual_gold_chance)
    #determine gold chance, then determine iridium chance, then subtract iridum amount, then gold amount from remainder, then rest is silver
    
determineIridiumQuality(13,3,1)
#digitize returns a list of length data in which each item in the index
# is a refers to each item in data (for example result[0] refers to which bin data[0] is assigned to)
# THIS digitize is good for continous data values, in the example below we are looking to assign the values in data to the bins 0 <= x < 2 (bin 1), 2 <= x < 5 (bin 2), 5 <= x < 10 (bin 3)
#this does NOT WORK for determining farming quality BECAUSE it is not continuous, we are determing the chance of being gold, then on the remainder the chance of being silver
#data = [1.5, 2.3, 4.5, 5.1, 7.8]
#bins = [0, 2, 5, 10]
#result = np.digitize(data, bins)



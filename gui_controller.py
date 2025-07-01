import sys
from stardew_valley import *
from error_no_harvests import *
from constants import *
from crop_controller import CropController
from seeds import Seed
import json


#from PyQt5.QtCore import Qt

class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.push_proceed.clicked.connect(self.accept)

class MyForm(QtWidgets.QMainWindow):
    def __init__(self, parents=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showFullScreen()

        #Add Subwindows, and while also removing the close button
        self.ui.mdiArea_main.addSubWindow(self.ui.subwindow_main_menu, QtCore.Qt.WindowType.FramelessWindowHint)
        self.ui.mdiArea_main.addSubWindow(self.ui.subwindow_planner, QtCore.Qt.WindowType.FramelessWindowHint)
        self.ui.mdiArea_table.addSubWindow(self.ui.subwindow_table, QtCore.Qt.WindowType.FramelessWindowHint)
        self.ui.mdiArea_table.addSubWindow(self.ui.subwindow_addcrop, QtCore.Qt.WindowType.FramelessWindowHint)

        #Default by maximising the main menu window, as well as the table window
        self.ui.subwindow_main_menu.showMaximized()
        self.ui.subwindow_table.showMaximized()

        #Subwindow Main Menu
        self.ui.push_exit.clicked.connect(self.close)
        self.ui.push_new.clicked.connect(self.toPlanner)

        #Subwindow Planner
        self.ui.push_return.clicked.connect(self.toMenu)

        #Subwindow Table
        self.ui.push_add_crop.clicked.connect(self.toAddCrop)

        #Subwindow AddCrop
        self.ui.push_cancel_add_crop.clicked.connect(self.toTable)
        self.ui.push_add_crop_final.clicked.connect(self.addCropToTable)
        self.ui.combo_season_planted.addItems(SEASONS)
        self.ui.combo_season_planted.currentIndexChanged.connect(self.updateComboSeedName)
        self.ui.checkBox_regrow.setChecked(True)
        self.ui.combo_fertilizer.addItem("None")
        self.ui.combo_fertilizer.addItems([str(key) for key in SPEED_FERTILISERS.keys()])
        self.ui.combo_fertilizer.addItems([str(key) for key in QUALITY_FERTILISERS.keys()]) 

        cropNames = CropController.getSeedNameFromSeason(self.ui.combo_season_planted.currentText())
        self.ui.combo_seed_name.addItems(cropNames)
        self.ui.spin_day_planted.setRange(1, 28)
        self.ui.spin_amount_purchased.setRange(1, 3000)
        
        

        #Adding columns to Table Planner
        self.ui.table_planner.setColumnCount(13)
        self.ui.table_planner.setHorizontalHeaderLabels(["Name", "Season/s", "Cost per Seed","Base Sell Price", "Grow Time", "Regrow Time", "Day Planted","Regrow/Replant?","Number of harvests","Amount Purchased","Fertiliser", "Total Cost","Estimated Profit"])
        header = self.ui.table_planner.horizontalHeader()
        for col in range(self.ui.table_planner.columnCount()):
            if col != 8:
                header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
                header.resizeSection(col, 250)

        #Initialising Farming Level and Perks
        self.ui.spinner_farming_level.setRange(0, 14)

    #Makes the planner subwindow the main subwindow
    def toPlanner(self):
        self.ui.subwindow_planner.showMaximized()
    #Makes the main menu subwindow the main subwindow    
    def toMenu(self):
        self.ui.subwindow_main_menu.showMaximized()

    #Makes table the focused subwindow of mdiArea_table
    def toTable(self):
        self.ui.subwindow_table.showMaximized()
        self.ui.push_save.show()
    #Makes add crop the focused subwindow of mdiArea_table
    def toAddCrop(self):
        self.ui.subwindow_addcrop.showMaximized()
        self.ui.push_save.hide()

    #Update the Seed Name combo with seeds of the currently selected season
    def updateComboSeedName(self):
        cropNames = CropController.getSeedNameFromSeason(self.ui.combo_season_planted.currentText())
        self.ui.combo_seed_name.clear()
        self.ui.combo_seed_name.addItems(cropNames)

        

    def addCropToTable(self):
        
        c = CropController(Seed.getSeedIDFromName(self.ui.combo_seed_name.currentText())) #initalise crop controller from name of seed
        if (self.ui.checkBox_regrow.isChecked()):
            dictHarvests = c.regrowableHarvest(self.ui.combo_season_planted.currentText(), self.ui.spin_day_planted.value(), self.ui.combo_fertilizer.currentText() )    
        else:
            dictHarvests = c.singleHarvest(self.ui.combo_season_planted.currentText(), self.ui.spin_day_planted.value())
   
            
        if(dictHarvests["Total"] != 0):
            tableInfo = c.getTableInformation()
            tableInfo.append(self.ui.spin_day_planted.value())
            tableInfo.append(self.ui.checkBox_regrow.isChecked()) 
            tableInfo.append(dictHarvests)
            tableInfo.append(self.ui.spin_amount_purchased.value()) 
            tableInfo.append(self.ui.combo_fertilizer.currentText())
            
            #Determine qualityOfCrops in a singleHarvest
            qualCrops = c.determineQualityOfHarvest(self.ui.spinner_farming_level.value(), self.ui.combo_fertilizer.currentText(), self.ui.spin_amount_purchased.value()) #5 is temp value until farming level is implemented in the ui\
            
            tableInfo.append(c.determineCost(self.ui.spin_amount_purchased.value()))#Cost
            tableInfo.append(c.determineEstimatedProfit(qualCrops, dictHarvests["Total"])) #Profit 
            

            row_count = self.ui.table_planner.rowCount()
            self.ui.table_planner.insertRow(row_count)
 
            for col, value in enumerate(tableInfo):
                self.ui.table_planner.setItem(row_count, col, QtWidgets.QTableWidgetItem(str(value)))   
        else:
            dialog = MyDialog()
            dialog.exec_()

 





        



            
        
        

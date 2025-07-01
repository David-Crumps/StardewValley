import sys
from database_manager import DatabaseManager
from seeds import Seed
from plant import Plant
from cropitem import CropItem
from crop_controller import CropController
from gui_controller import *
import json


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())




    





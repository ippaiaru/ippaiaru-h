from src.gui.GUIClass import GUIClass
from src.gui.baseClass import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = GUIClass()
    ui.show()
    sys.exit(app.exec_())

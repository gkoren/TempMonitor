import sys
from PyQt4 import QtGui
from mainWindow import Ui_MainWindow

class TempGui(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TempGui()
    window.show()
    sys.exit(app.exec_())

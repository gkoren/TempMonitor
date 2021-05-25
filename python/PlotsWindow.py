# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PlotsWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PlotsWindow(object):
    def setupUi(self, PlotsWindow):
        PlotsWindow.setObjectName(_fromUtf8("PlotsWindow"))
        PlotsWindow.resize(640, 480)
        PlotsWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtGui.QWidget(PlotsWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plots_container = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plots_container.sizePolicy().hasHeightForWidth())
        self.plots_container.setSizePolicy(sizePolicy)
        self.plots_container.setObjectName(_fromUtf8("plots_container"))
        self.plots_Layout = QtGui.QVBoxLayout(self.plots_container)
        self.plots_Layout.setObjectName(_fromUtf8("plots_Layout"))
        self.gridLayout.addWidget(self.plots_container, 0, 1, 1, 1)
        self.plots_list = QtGui.QListWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plots_list.sizePolicy().hasHeightForWidth())
        self.plots_list.setSizePolicy(sizePolicy)
        self.plots_list.setMaximumSize(QtCore.QSize(160, 16777215))
        self.plots_list.setObjectName(_fromUtf8("plots_list"))
        self.gridLayout.addWidget(self.plots_list, 0, 2, 1, 1)
        PlotsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PlotsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        PlotsWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PlotsWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PlotsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PlotsWindow)
        QtCore.QMetaObject.connectSlotsByName(PlotsWindow)

    def retranslateUi(self, PlotsWindow):
        PlotsWindow.setWindowTitle(_translate("PlotsWindow", "MainWindow", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PlotsWindow = QtGui.QMainWindow()
    ui = Ui_PlotsWindow()
    ui.setupUi(PlotsWindow)
    PlotsWindow.show()
    sys.exit(app.exec_())


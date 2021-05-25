#!/usr/bin/python

#from PyQt4.uic import loadUiType
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PlotsWindow import Ui_PlotsWindow
from matplotlib.lines import Line2D

#import matplotlib.pyplot as plt
import numpy as np

#Ui_MainWindow, QMainWindow = loadUiType('plots_area.ui')

class plots_window(QMainWindow, Ui_PlotsWindow):
    def __init__(self, parent=None):
        super(plots_window, self).__init__(parent)
        self.setupUi(self)
        self.canvas = LiveCanvas()
        self.plots_Layout.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self.plots_container, coordinates=True)
        #self.plots_Layout.addWidget(self.canvas)
        self.plots_Layout.addWidget(self.toolbar)
        self.on_show = False
        self.plots_dict = {}
        self.current_plot = 0 #Default is all sensors
        self.plots_list.itemClicked.connect(self.change_figure)
        #self.plots_list.addItem(name)
        #plot.plot([],[]])
        #plot.plot(self.data[0][-20:],self.data[1][-20:])
        #self.plot.set_title("Temp1")

    def add_list_entry(self,index,name):
        self.plots_list.addItem(name)
        self.plots_dict[name] = index
        #Temp for controlling the figure"

    def clear_plots_list(self):
        self.plots_list.clear()

    def change_figure(self,item):
        text = item.text()
        self.current_plot = self.plots_dict[str(text)]
        self.canvas.current_plot = self.plots_dict[str(text)]
        #self.canvas.update_canvas(xdata,ydata)


class LiveCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.plot = self.fig.add_subplot(111)
        self.xdata = []
        self.ydata = []
        self.current_plot = 1

        FigureCanvas.__init__(self,self.fig)

    def update_canvas(self,xdata,ydata):
        self.plot.clear()
        self.plot.set_xlabel("Time [s]")
        self.plot.set_ylabel("Temperature [C]")
        if self.current_plot == 0 and isinstace(ydata[0],list):
            self.plot.set_title("All Sensors")
            all_data = []
            colors = ["blue", "red","black", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "silver", "teal", "yellow"]
            self.plot.grid(True)
            for i,iList in enumerate(ydata):
                self.plot.plot(xdata,iList,label="Sensor "+str(i+1),color=colors[i])
        else:
            self.plot.set_title("Sensor "+str(self.current_plot))
            self.plot.set_autoscaley_on(True)
            self.plot.plot(xdata,ydata)
            self.plot.grid(True)
            self.plot.set_ylim(min(ydata)*0.95,max(ydata)*1.05)

        self.draw()


    def draw_all_sensors(self,xdata,all_ydata):
        self.plot.clear()
        self.plot.set_xlabel("Time [s]")
        self.plot.set_ylabel("Temperature [C]")
        self.plot.set_title("All Sensors")
        #self.plot.plot(xdata,ydata)
        self.plot.grid(True)
        all_temps = []
        #max_val = 0
        #min_val = 1000
        colors = ["blue", "red","black", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "silver", "teal", "yellow"]
        for i,iList in enumerate(all_ydata):
            all_temps.append(max(iList))
            all_temps.append(min(iList))
            self.plot.plot(xdata[-20:],iList[-20:],label="Sensor "+str(i+1),color=colors[i])
        self.plot.set_ylim(min(all_temps)*0.95,max(all_temps)*1.05)
        legend = self.plot.legend()
        self.draw()

        #self.plot.set_ylim(min(ydata)*0.95,max(ydata)*1.05)

    #self.show()

        #plt.figure()
        #self.canvas = FigureCanvas(self.figure)

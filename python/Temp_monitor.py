
#Temperature monitor. Reads data from MAX 3675 temperature sensor via Arduino Mega through serial com port.

import random,sys
sys.path.append("python")
sys.path.insert(0,"gui")
import Queue,csv,time
from com_monitor import ComMonitorThread
from wifi_monitor import WifiMonitorThread
from live_feed import LiveDataFeed,get_queue_all,get_queue_item
from dataTable_model import dataTableModel
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from MainWindow import Ui_MainWindow
from PlotsWindow import Ui_PlotsWindow
from plots_area import plots_window,LiveCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.lines import Line2D
##### Class for the main window operation ######
####################################################
class TempMonitor(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(TempMonitor,self).__init__(parent)
        self.setupUi(self)

        self.monitor_active = False
        self.wifi_monitor = None
        self.com_monitor = None
        self.com_data_q = None
        self.com_error_q = None
        self.com_portname = None
        self.com_baudrate = None
        self.wifi_ip = None
        self.wifi_port = None
        self.livefeed = LiveDataFeed()
        self.LiveCanvas = None
        self.nSensors = None
        self.data = [[]]
        self.averages = []
        self.displayData = [[]] #include one list for time, sensors list added late [time,temp1,temp2,...]
        #self.dataTable = QTableView()
        self.start_time = None
        self.timer = QTimer()
        self.plotsWindow = plots_window(self)

        self.btn_wifi.setChecked(True)
        self.set_wifi_mode()
        #self.box_serial_settings.setEnabled(False)
        self.btn_serial.clicked.connect(self.set_serial_mode)
        self.btn_wifi.clicked.connect(self.set_wifi_mode)

        self.btn_export_data.clicked.connect(self.save_file)
        self.btn_sensor_stats.clicked.connect(self.show_plots_window)
        self.btn_Stop.setEnabled(False)
        self.btn_sensor_stats.setEnabled(False)
        self.btn_export_data.setEnabled(False)

############ Selecting connetion type: Serial / Wifi ####################
    def set_wifi_mode(self):
        self.box_serial_settings.setEnabled(False)
        self.box_wifi_settings.setEnabled(True)
        self.btn_Start.clicked.connect(self.start_wifi_feed)
        try: self.btn_Start.clicked.disconnect(self.feed_start)
        except Exception: pass
        self.btn_Stop.clicked.connect(self.stop_wifi_feed)
        try: self.btn_Stop.clicked.disconnect(self.feed_stop)
        except Exception: pass

    def set_serial_mode(self):
        self.box_wifi_settings.setEnabled(False)
        self.box_serial_settings.setEnabled(True)
        self.btn_Start.clicked.connect(self.feed_start)
        try: self.btn_Start.clicked.disconnect(self.start_wifi_feed)
        except Exception: pass
        self.btn_Stop.clicked.connect(self.feed_stop)
        try: self.btn_Stop.clicked.disconnect(self.stop_wifi_feed)
        except Exception: pass


############ Controlling the feed: start,stop,update,loop #################
    def stop_wifi_feed(self):

        self.timer.stop()
        if self.wifi_monitor is not None:
            self.wifi_monitor.join()
            self.wifi_monitor = None

        self.monitor_active = False
        self.save_file()

        self.nSensors = None
        self.data = [[]]
        self.displayData = [[]]
        self.averages = []

        self.update_dataTable()
        self.plotsWindow.plots_list.clear()
        self.plotsWindow.close()

        self.btn_Start.setEnabled(True)
        self.btn_Stop.setEnabled(False)
        self.btn_serial.setEnabled(True)
        self.btn_wifi.setEnabled(True)
        self.btn_sensor_stats.setEnabled(False)
        self.btn_export_data.setEnabled(False)

    def start_wifi_feed(self):
        if self.wifi_monitor is not None:# or self.portname.text() == '':
            return

        self.start_time = time.localtime(time.time())

        self.data_q = Queue.Queue()
        self.error_q = Queue.Queue()
        self.wifi_ip = str(self.lineEdit_wifi_IP.text())
        self.wifi_port = int(self.lineEdit_wifi_port.text())
        self.wifi_monitor = WifiMonitorThread(self.data_q,self.error_q,self.wifi_ip,self.wifi_port)
        self.wifi_monitor.start()


        com_error = get_queue_item(self.error_q)
        if com_error is not None:
            QMessageBox.critical(self, 'WifiMonitorThread error',com_error)
            self.wifi_monitor = None
            return

        self.monitor_active = True
        while self.nSensors is None:
            self.find_sensors()
        for i in range(self.nSensors):
            self.data.append([])
            self.displayData.append([])
            #self.averages.append([])
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL('timeout()'), self.feed_loop)
        self.timer.start(2000.)

        self.btn_Start.setEnabled(False)
        self.btn_Stop.setEnabled(True)
        self.btn_sensor_stats.setEnabled(True)
        self.btn_export_data.setEnabled(True)

    def update_wifi_feed(self):

        if self.livefeed.has_new_data:
            this_data = self.livefeed.read_data()
            print this_data
            if len(self.displayData[0]) > 20:
                for iList in self.displayData:
                    iList.pop()
            self.data[0].append(this_data["timestamp"])
            self.displayData[0].insert(0,this_data["timestamp"])
            self.averages = []
            self.averages.append([this_data["timestamp"]])
            for i,temp_i in enumerate(this_data["temperatures"]):
                self.data[i+1].append(float(temp_i))
                self.displayData[i+1].insert(0,str(temp_i))
                self.averages.append([sum(self.data[i+1])/len(self.data[0])])
                #self.create_plots()
                #self.averages.appens(0)
            return True

        return False

    def feed_stop(self):

        self.timer.stop()
        if self.com_monitor is not None:
            self.com_monitor.join()
            self.com_monitor = None

        self.monitor_active = False
        self.save_file()

        self.nSensors = None
        self.data = [[]]
        self.displayData = [[]]
        self.averages = []

        self.update_dataTable()
        self.plotsWindow.plots_list.clear()
        self.plotsWindow.close()

        self.btn_Start.setEnabled(True)
        self.btn_Stop.setEnabled(False)
        self.btn_sensor_stats.setEnabled(False)
        self.btn_export_data.setEnabled(False)

    def feed_start(self):

        if self.com_monitor is not None:# or self.portname.text() == '':
            return

        self.start_time = time.localtime(time.time())
        #self.btn_Start.setText("Stop")
        #self.btn_Start.clicked.connect(self.feed_stop)

        self.data_q = Queue.Queue()
        self.error_q = Queue.Queue()
        self.com_portname = str(self.lineEdit_serial_port.text())
        self.com_baudrate=int(self.combo_serial_baudrate.currentText())
        self.com_monitor = ComMonitorThread(self.data_q,self.error_q,self.com_portname,self.com_baudrate)
        self.com_monitor.start()

        com_error = get_queue_item(self.error_q)
        if com_error is not None:
            QMessageBox.critical(self, 'ComMonitorThread error',com_error)
            self.com_monitor = None
            return

        self.monitor_active = True
        while self.nSensors is None:
            self.find_sensors()
        for i in range(self.nSensors):
            self.data.append([])
            self.displayData.append([])
            #self.averages.append([])
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL('timeout()'), self.feed_loop)
        self.timer.start(2000.)

        self.btn_Start.setEnabled(False)
        self.btn_Stop.setEnabled(True)
        self.btn_sensor_stats.setEnabled(True)
        self.btn_export_data.setEnabled(True)

    def feed_update(self):

        if self.livefeed.has_new_data:
            this_data = self.livefeed.read_data()
            print this_data
            if len(self.displayData[0]) > 20:
                for iList in self.displayData:
                    iList.pop()
            self.data[0].append(this_data["timestamp"])
            self.displayData[0].insert(0,this_data["timestamp"])
            self.averages = []
            self.averages.append([this_data["timestamp"]])
            for i,temp_i in enumerate(this_data["temperatures"]):
                self.data[i+1].append(float(temp_i))
                self.displayData[i+1].insert(0,str(temp_i))
                self.averages.append([sum(self.data[i+1])/len(self.data[0])])
                #self.create_plots()
                #self.averages.appens(0)
            return True

        return False

    def feed_loop(self):
        #self.dummy_func()
        self.read_serial_data()
        if self.feed_update():
            self.update_dataTable()
        if self.plotsWindow.on_show:
            if self.plotsWindow.current_plot is not 0:
                self.plotsWindow.canvas.update_canvas(self.data[0][-20:],self.data[self.plotsWindow.current_plot][-20:])
            else:
                self.plotsWindow.canvas.draw_all_sensors(self.data[0],self.data[1:])
################# Actions while running the scan: ###############
################ find the sensors, read data, save data, update table, update buttons #################

    def find_sensors(self):
        qdata = list(get_queue_all(self.data_q))

        if len(qdata) > 0:
            all_temps_string = qdata[-1][0].split(",")
            self.nSensors = len(all_temps_string)
            print str(self.nSensors)+" sensors found"
            return True
        else:
            return False

    def read_serial_data(self):
        qdata = list(get_queue_all(self.data_q))
        if len(qdata) > 0:
            data = dict(timestamp=qdata[-1][1],
                        temperatures=qdata[-1][0].strip("\r\n").split(","))
                        #temperatures=qdata[-1][0][:-2].split(","))
            self.livefeed.add_data(data)

    def save_file(self):
        choice = QMessageBox.question(self, 'Save data',
                                            "Export data to Excel?",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.export_to_csv()
        else:
            pass

    def export_to_csv(self,outDir='',outFileName='temp_monitor'):
        timestamp = self.start_time
        timestring = str(timestamp[2])+"_"+str(timestamp[1])+"_"+str(timestamp[0])+"_"+str(timestamp[3])+"_"+str(timestamp[4])
        if outDir:
            outDir+="/"
        outF = open(outDir+outFileName+"_"+timestring+".csv","wb")
        writer = csv.writer(outF)
        headers = ["Time"]
        for i in range(1,len(self.data)):
            headers.append("Temp"+str(i))
        writer.writerow(headers)
        writer.writerows(map(list,zip(*self.data)))
        outF.close()
        return

    def btn_enable_state(self):
        if self.com_portname is None:
            start_enable = stop_enable = False
        else:
            start_enable = not self.monitor_active
            stop_enable = self.monitor_active

    def update_dataTable(self):
        headers = ["Time"]
        avg_headers = ["Time"]
        for i in range(1,len(self.data)):
            headers.append("Temp"+str(i))
            avg_headers.append("Avg Temp"+str(i))
        this_data = map(list,zip(*self.displayData))
        this_avgs = map(list,zip(*self.averages))

        t_model = dataTableModel(this_data, headers)
        self.tableView_data.setModel(t_model)
        self.tableView_data.setShowGrid(False)
        self.tableView_data.verticalHeader().setVisible(False)
        self.tableView_data.horizontalHeader().setStretchLastSection(False)
        #self.tableView.resizeRowsToContents()
        #self.tableView.resizeColumnsToContents()
        avg_model = dataTableModel(this_avgs, avg_headers)
        self.tableView_avg.setModel(avg_model)
        self.tableView_avg.setShowGrid(False)
        self.tableView_avg.verticalHeader().setVisible(False)
        self.tableView_avg.horizontalHeader().setStretchLastSection(False)

############## Controlling the plots window: ###############
################# Open,create,update #####################

    def setup_plots_list(self):
        self.plotsWindow.clear_plots_list()
        for i in range(self.nSensors+1):
            if i == 0:
                self.plotsWindow.add_list_entry(i,"All Sensors")
            else:
                self.plotsWindow.add_list_entry(i,"Sensor "+str(i))

    @pyqtSlot()
    def show_plots_window(self):
        self.plotsWindow.on_show = True
        self.setup_plots_list()
        self.plotsWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TempMonitor()
    window.show()
    sys.exit(app.exec_())

# TempMonitor

This project contains the code + instructions for a temperature monitoring system. It is based on a number of temperature sensors (k-type thermocouples) connected to an Arduino Mega board. The sensors are placed in a number of locations and thry constantly send real-time temperature data to a computer via Wifi (UDP). A dedicated GUI is designed to control the measurement, monitor the temperatures, and export the data to csv for further offline analysis.

This project was originally made as part of my PhD work. It was designed to test the cooling system for the electronic readout boards placed on the sTGC detector, which is part of the Muon-Spectrometer in the ATLAS experiment @ LHC, CERN.  

### Hardware

The temperature monitoring system contains four main components:
1. Arduino Mega 2560 controller
1. MAX 6673 k-type thermocouples
1. ESP 2866 Wifi micro-chip
1. 5.0V/3.3V Level-Shifter

A sketch illustrating how to connect the components is available in [/doc/FullSetup.jpg](https://github.com/gkoren/TempMonitor/blob/master/doc/FullSetup.jpg)

Eventually we designed a specail board that can be placed on top of the Arduino controller with the other componnents connected to it:  
    ![CustomSetup](/doc/CustomSetup.png)
    
      
   Here in the picture a single thermocouple sensor is connected to the system. In principle it is possible in this setup to connect up to 9 sensors simultaneously.
   
   
### Software

The code for running the monitoring system can be generally split into two main parts. One that activates the measurements via the Arduino controller, and one that activates and control the GUI (Python+Qt4)  
Arduino has great documentation, and if there are any parts I left out you can look for info in their web page: https://www.arduino.cc/ or simply google the issue – there are usually answers there.

#### Step 1 : Arduino code

Before going into specific instructions for this project, you'll need to download and install the Arduion IDE which allows to upload code onto the Arduino. Once the code is uploaded on the Arduino it should run in the background regardless of the GUI.

In the "/Arduino" folder there are 3 subfolders: 2 containing the code files (one for serial communication and one for wifi communication via UDP),
and another folder with necessary libraries (don't need to do anything with these files, just have them saved). Note: this documenation contains instructions only for monitoring via Wifi communication.

1. **Connecting the Arduino to a Wifi network:**
    1. Connect the Arduino board to your computer USB port and open the file "Arduino/ESP_dialog/ESP_dialog.ino". This script will allow to communicate and gove commands directly to the Wifi chip.  
    Upload the script to the Arduino by clicking 'Upload' button (top left) and then wait to receivethe 'Done Uploading' message (bottom left)    
              
        ![Readme1](/doc/images/Readme/1.png)  
        
          
    1. Click on the 'Serial Monitor' button (top right) to type commands to the board. Make sure that the settings in the bottom are set like in the picture. Type `AT` in the command line and then press 'Enter/Send'. Wait to receive the 'OK' mesaage back on the screen.  
          
        ![Readme3](/doc/images/Readme/3.png)  
    
    1. Type the following commands:
    * `AT+RST` (Resets the Wifi chip)
    * `AT+CWLAP` (Prints a list of available networks). 
        * Make sure the desired network (same one your computer is connected to) appears in the list.
    * `AT+CWJAP="<network_name>","<password>"` (connects the Wifi chip to the network)
    
    After sending these commands wait to see the message: 'Wifi Connected' followed by 'Wifi Got IP'
                
    ![Readme4](/doc/images/Readme/4.png)  
    
1. **Sending and reading data:**
    1. Now we want to tell the Arduino to read the temperature data and send it to the computer. To do so open the file "/Arduino/Read_Temperature_Wifi/Read_Temperature_Wifi.ino".
    1. Before uploading the script to the Arduino, we first need to type in the IP address of the computer. In the line that reads `#define HOST_NAME XX.XX.XX.XX` replace the IP address with that of your computer (you **don't** need to edit the "HOST_PORT")
    2. Make sure that the line reads `int n_Sensors` matches the number of sensors you have connected to the Arduino. 
    3. After the correct IP adress is updated, save the file and upload the code to the Arduino board (top left)  
          
        ![Readme5](/doc/images/Readme/5b.png)  
        
#### Step 2 : Python code / TempMonitor GUI

The code that controls the GUI is based on python+Qt4 and is stored inside the "/pytohn/" directory.   
Now that the Arduino code runs in the background and temperature data is being sent to the computer, we can run the GUI and display the data on the screen. 

1. There are two ways to run the GUI:
    * (Windows only): simplest way is using the executable "/dist/Temp_monitor.exe". To open the GUI this way you don't need to have python installed on your computer, and it should more or less run out of the box.   
    Note that there are quote a lot of files in the ".dist/" directory, which are  byproduct of bundling the python files and creating the executable. You only need to use "Temp_monitor.exe"
    * Using the pytohn scripts (Mac/Linux/Windows): to run the GUI this way you'll need to have 'python 2.7' or higher installed on your computer and install the additional libraries:
        * Matplotlib
        * Pyserial
        * PyQt4  
        
    To activate the GUI simply type: `python -u Temp_monitor.py`
1. Make sure the option 'Wifi' is checked, and fill in the IP and PORT as they appear in the Arduino script uploaded on the controller ("/Arduino/Read_Temperature_Wifi/Read_Temperature_Wifi.ino")
2. Press 'Start' to begin collecting data. Within a few seconds the temperatures should appear on the screen.   
    
    ![Readme6](/doc/images/Readme/6.png)    
    
4. You can click 'Sensor Statistics' to display a plot of *temperature vs time* for all the connected sensors, and then select to display only a specifc sensors from the window on the right.  
    ![Readme7](/doc/images/Readme/7.png)    
    
6. When pressing 'Stop' you will be asked if you want to save the data as a .csv file (or altenratively you can click 'Export to Excel' in any time). The data will be save in the main directory with a name matching the timestamp of the measurement. **It is recommended to rename the file after saving it. It will otherwise be hard to distinguish between different files.**


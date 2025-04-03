# Author: Mohamed Habib Ben Abda
# Date: Fall semester 2024
# Mapping window
import sys
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication
from PyQt5.uic import loadUi
import serial
import time
from API.ds8r_controller import DS8RController
from API.d188_controller import D188Controller

stimulator = DS8RController()
selector = D188Controller()
uC = None # Will take serial instance

class Mapping_view(QMainWindow):
    def __init__(self):
        super(Mapping_view,self).__init__()
        loadUi("QtDesigner//gui_mapping.ui",self)
        # Setting up acceptable parameters
        self.setup_param_ranges()
        self.update_SB_IP_setup(self.SB_IP.value())
        self.SB_IP.valueChanged.connect(self.update_SB_IP_setup)
        # Initialise the D128Controller
        self.init_DS8RController()
        self.init_selector()
        # Initialise the uC
        self.init_uC_comm()
        # Initialise the paramters
        self.init_param_values()
        self.update_DS8R()
        # Initialise the trigger value
        self.trigger = False

        self.PB_UPDATE.clicked.connect(self.update_DS8R)
        self.CB_CH.currentTextChanged.connect(self.on_channel_changed)
        self.PB_START_STOP.clicked.connect(self.start_stop)

    def setup_param_ranges(self):
        self.SB_PA.setRange(0.0, 50.0) # Stop user from intering dangerous current amplitude here
        self.SB_PA.setDecimals(1)
        self.SB_PA.setSingleStep(0.1)
        
        self.SB_PW.setRange(50, 2000)
        self.SB_PW.setSingleStep(10)
        
        self.SB_IP.setRange(1, 990)
        
        self.SB_RP.setRange(10, 100)
        self.SB_RP.setSingleStep(1)

        self.SB_F.setRange(0, 1000)
        self.SB_F.setSingleStep(1)
    
    '''
    Update the singleStep based on the current value of the spin box.
    '''
    def update_SB_IP_setup(self, value):
        if (value == 1):
            self.SB_IP.setSingleStep(9)
        else:    
            self.SB_IP.setSingleStep(10)

    def init_param_values(self):
        self.CB_M.setCurrentIndex(1)
        self.CB_POL.setCurrentIndex(0)
        self.CB_S.setCurrentIndex(0)
        self.SB_PA.setValue(1)
        self.SB_PW.setValue(1000)
        self.SB_IP.setValue(1)
        self.SB_RP.setValue(100)
        self.SB_F.setValue(1)

    def init_DS8RController(self):
        stimulator.Initialise()
        stimulator.Enable(False)
        stimulator.Close()  
        time.sleep(0.1)

    def init_selector(self):
        selector.Initialise()
        selector.SetMode('USB')
        selector.SetIndicator('ON')
        selector.SetDelay(1) # 1ms (can go up to 0.1ms but don't need to here)
        selector.SetChannel(1)
        selector.Close()

    def init_uC_comm(self):
        '''
        Establish serial communication with uC
        '''
        try:
            # Attempt to open the serial port
            global uC
            uC = serial.Serial('COM5', 115200, timeout=1)  # Replace 'COM3' with your port
            
            # Allow time for the connection to establish
            time.sleep(1.5)  
            
            # Check if the port is open
            if uC.is_open:
                print("Serial port opened successfully.")
            else:
                print("Failed to open the serial port.")
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    def update_DS8R(self):

        stimulator.Initialise()

        stimulator.Cmd('mode', self.CB_M.currentText())
        stimulator.Cmd('polarity', self.CB_POL.currentText())
        stimulator.Cmd('source', self.CB_S.currentText())
        stimulator.Cmd('demand', self.SB_PA.value())
        stimulator.Cmd('pulsewidth', self.SB_PW.value())
        stimulator.Cmd('dwell', self.SB_IP.value())
        stimulator.Cmd('recovery', self.SB_RP.value())

        stimulator.Close()
        time.sleep(0.1)

    def on_channel_changed(self, channel_str):
        channel = int(channel_str)
        selector.Initialise()
        selector.SetChannel(channel)
        selector.Close()
        time.sleep(0.2)

    def start_stop(self):
        freq = self.SB_F.value()
        if self.trigger == False:
            # Enable the device
            stimulator.Initialise()
            stimulator.Enable(True)
            stimulator.Close()                                
            time.sleep(0.1)
            command = 'start:' + str(freq) + '\n'
            uC.write(command.encode())
            self.trigger = True
        else:
            command = 'stop\n'
            uC.write(command.encode())
            # disable the device
            stimulator.Initialise()
            stimulator.Enable(False)
            stimulator.Close()                                
            time.sleep(0.1)
            self.trigger = False

    def close_uC_comm(self):
        if self.trigger == True:
            command = 'stop\n'
            uC.write(command.encode())
        try:     
            if uC.is_open:
                uC.close()
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        stimulator.Close()
        time.sleep(0.1)
        selector.Close()
        time.sleep(0.1)

    def closeEvent(self, event):
        self.close_uC_comm()  # Call your function before closing
        event.accept()  # Accept the close event

if __name__ == '__main__':
    # Start mapping window
    app = QApplication(sys.argv)
    mapping_window = Mapping_view()
    mapping_window.show()
    app.exec_()
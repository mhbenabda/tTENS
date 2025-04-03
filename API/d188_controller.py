# Author: Mohamed Habib Ben Abda
# Date: Fall semester 2024
# API for D188 Digitimer Electrode Selector
from ctypes import Structure, c_ubyte, c_ushort, c_int, WINFUNCTYPE, c_void_p, byref, WinDLL #, sizeof, cast
from sys import getsizeof

hDGD188Api = WinDLL("DGD188API.DLL")

# ------------------------------------------------------------------------------
# Declare D188 classes 
class D188STATE_T(Structure):
    _fields_ = [
        ("D188_Mode", c_ubyte),       # Mode: 0 = OFF, 1 = USB, 2 = TTL (1-8), 3 = TTL (4-8)
        ("D188_Select", c_ubyte),     # Select: 0 = All channels off, 1 = Channel 1, ..., 128 = Channel 8
        ("D188_Indicator", c_ubyte),  # Indicator: 0 = OFF, !0 = ON
        ("D188_Delay", c_ushort)      # Delay in 100us units between change detection and application
    ]

class D188DEVICESTATE_T(Structure):
    _fields_ = [
        ("D188_DeviceID", c_int),
        ("D188_VersionID", c_int),
        ("D188_Error", c_int),
        ("D188_State", D188STATE_T)
    ]

class DEVHDR(Structure):
    _fields_ = [
        ("DeviceCount", c_int)
    ]

class D188(Structure):
    _fields_ = [
        ("Header", DEVHDR),
        ("State", D188DEVICESTATE_T)
    ]

# ------------------------------------------------------------------------------
# Declare DLL API function and associated parameters
protoDGD188_Initialise = WINFUNCTYPE (
    c_int,       #Function result
    c_void_p,    #Instance Reference
    c_void_p,    #Initialise Result
    c_int,       #Callback pointer (not used MUST be 0)
    c_int        #Callback parameters (not used MUST be 0)
    )

protoDGD188_Update = WINFUNCTYPE (
    c_int,       #Function result
    c_int,       #Instance Reference
    c_void_p,    #Update Result
    c_void_p,    #NewState
    c_int,       #cbNewState
    c_void_p,    #CurrentState
    c_void_p,    #cbCurrentState
    c_int,       #Callback pointer (not used MUST be 0)
    c_int        #Callback parameters (not used MUST be 0)
    )

protoDGD188_Close = WINFUNCTYPE (
    c_int,       #Function result
    c_void_p,    #Instance Reference
    c_void_p,    #Close Result
    c_int,       #Callback pointer (not used MUST be 0)
    c_int        #Callback parameters (not used MUST be 0)
    )


paramsDGD188_Initialise = (1,"Reference",0),(1,"InitResult",0),(1,"CallbackProc",0),(1,"CallbackParam",0),
paramsDGD188_Update =  (1,"Reference",0),(1,"updateResult",0),(1,"NewState",0),(1,"cbNewState",0),(1,"CurrentState",0),(1,"cbCurrentState",0),(1,"CallbackProc",0),(1,"CallbackParam",0),
paramsDGD188_Close =  (1,"Reference",0),(1,"CloseResult",0),(1,"CallbackProc",0),(1,"CallbackParam",0),


DGD188_Initialise = protoDGD188_Initialise(("DGD188_Initialise",hDGD188Api), paramsDGD188_Initialise)
DGD188_Update = protoDGD188_Update(("DGD188_Update",hDGD188Api), paramsDGD188_Update)
DGD188_Close = protoDGD188_Close(("DGD188_Close",hDGD188Api), paramsDGD188_Close)

# ------------------------------------------------------------------------------
# Declare D188 class
class D188Controller:
    def __init__(self):
        self.apiRef = c_int(0)          
        self.retError = c_int(0)         
        self.retAPIError = c_int(0)   
        self.closeResult = c_int(0)   

        self.D188Mode = {
            'OFF': c_ubyte(0),
            'USB': c_ubyte(1),
            '8TTL': c_ubyte(2),
            '4TTL': c_ubyte(3)
        }

        self.D188Select = {
            0: c_ubyte(0),          # All channels off
            1: c_ubyte(1),          # Channel 1 selected
            2: c_ubyte(2),          # ...    
            3: c_ubyte(4),
            4: c_ubyte(8),
            5: c_ubyte(16),
            6: c_ubyte(32),
            7: c_ubyte(64),
            8: c_ubyte(128)
        }

        self.D188Indicator = {
            'OFF': c_ubyte(0),          # 0 = Channel active indicators OFF
            'ON': c_ubyte(1)           # !0 = Channel active indicators ON
        }

    def Initialise(self):
        '''
        Must be the first function called to initialise the D188 stack and return an
        instance reference.
        '''        
        self.apiRef = c_int(0)
        self.retAPIError = c_int(0)
        return DGD188_Initialise(byref(self.apiRef), byref(self.retAPIError), 0,0)
    
    def Close(self):
        '''
        Close and free all resources associated with the instance reference (apiRef).
        Called once D188 has been finished with. It is advisable to hold on to the
        refernce until the end of the program
        '''
        self.closeResult = c_int(0)
        DGD188_Close(byref(self.apiRef), byref(self.closeResult), 0,0)

    def UpdateGet(self, STATE):
        '''
        Fetch the current state associated with the supplied instance reference.
        '''         
        self.retAPIError = c_int(0)  
        _STATE = D188()
        _cbSTATE = c_int(getsizeof(_STATE))
        DGD188_Update(self.apiRef, byref(self.retAPIError), 0, 0, byref(_STATE), byref(_cbSTATE), 0,0)
        STATE.Header = _STATE.Header
        STATE.State = _STATE.State
    
    def UpdateSet(self, STATE):
        '''
        Takes an object of type D188 and updates the connected device to match the state
        '''
        self.retAPIError = c_int(0)  
        _STATE = D188()
        _cbSTATE = c_int(getsizeof(_STATE))
        _STATE.Header = STATE.Header
        _STATE.State = STATE.State
        DGD188_Update(self.apiRef, byref(self.retAPIError), byref(_STATE), _cbSTATE, 0, 0, 0,0)

    def SetChannel(self, channel):
        '''
        Set which channel is active
        Args:
            channel (self.D1288Select): 0,1,2,...,8
        '''
        if channel in self.D188Select:
            STATE = D188()
            self.UpdateGet(STATE)
            STATE.State.D188_State.D188_Select = self.D188Select[channel]
            self.UpdateSet(STATE)
        else:
            print('ERROR! Channel argument invalid')
    
    def SetMode(self, mode):
        '''
        Set which controll mode is used for the selector
        Args:
            mode (self.D1288Mode): 'OFF', 'USB', '8TTL' or '4TTL'
        '''
        if mode in self.D188Mode:
            STATE = D188()
            self.UpdateGet(STATE)
            STATE.State.D188_State.D188_Mode = self.D188Mode[mode]
            self.UpdateSet(STATE)
        else:
            print('ERROR! Mode argument invalid')

    def SetIndicator(self, indicator):
        '''
        Set if LED indicators are activated/disactivated
        Args:
            indicator (self.D188Indicator): 'ON' or 'OFF'
        '''
        if indicator in self.D188Indicator:
            STATE = D188()
            self.UpdateGet(STATE)
            STATE.State.D188_State.D188_Indicator = self.D188Indicator[indicator]
            self.UpdateSet(STATE)
        else:
            print('ERROR! Indicator argument invalid')

    def SetDelay(self, delay):
        '''
        Set the The Delay/De-bounce setting
        D188_Delay DLL argument takes n = number of 100us to delay between detecting a change on the rear
        panel socket and applying the change to the selected channels.
        Args:
            delay (float): between 0.1-1000 milliseconds
        '''
        if 0.1 <= delay <= 1000:
            STATE = D188()
            self.UpdateGet(STATE)
            n = int(delay * 1000 / 100)     # convert to us and devide by 100us to get n 
            c_n = c_ushort(n)              # devide by 100us to get n 
            STATE.State.D188_State.D188_Delay = c_n
            self.UpdateSet(STATE)
        else:
            print('ERROR! Indicator argument invalid')

    def PrintState(self):
        '''
        Print the current content of the D188 STATE
        '''
        STATE = D188()
        self.UpdateGet(STATE)
        print(
            {
                'D188_Mode': STATE.State.D188_State.D188_Mode,
                'D188_Select': STATE.State.D188_State.D188_Select,
                'D188_Indicator': STATE.State.D188_State.D188_Indicator,
                'D188_Delay': STATE.State.D188_State.D188_Delay,
                'D188_DeviceID': STATE.State.D188_DeviceID,
                'D188_VersionID': STATE.State.D188_VersionID,
                'D188_Error': STATE.State.D188_Error,
                'DeviceCount': STATE.Header.DeviceCount
            }
        )

if __name__ == "__main__":
    d188 = D188Controller()
    d188.Initialise()
    d188.SetChannel(3)
    d188.SetDelay(1)
    d188.SetIndicator('ON')
    d188.SetMode('USB')
    d188.PrintState()
    d188.Close()

# Author: Mohamed Habib Ben Abda
# Date: Fall semester 2024
# API for DS8R Digitimer Stimulator
from ctypes import c_int, c_uint, c_void_p, Structure, Union, WINFUNCTYPE, LittleEndianStructure, byref, WinDLL
from sys import getsizeof

hDGD128Api = WinDLL("D128API.DLL")

# ------------------------------------------------------------------------------
# Declare DS8R classes 
class STATEFLAGS(Union):
    class _Bits(LittleEndianStructure):
        _fields_ = [
            ("OVERENERGY", c_uint, 1),
            ("HWERROR", c_uint, 1),
            ("reserved", c_uint, 30),
        ]
    _anonymous_ = ("bits",)
    _fields_ = [
        ("bits", _Bits),
        ("VALUE", c_int),
    ]

class CONTROLFLAGS(Union):
    class _Bits(LittleEndianStructure):
        _fields_ = [
            ("ENABLE", c_int, 2),
            ("MODE", c_int, 3),
            ("POLARITY", c_int, 3),
            ("SOURCE", c_int, 3),
            ("ZERO", c_int, 2),
            ("TRIGGER", c_int, 2),
            ("NOBUZZER", c_int, 2),
            ("RESERVED", c_int, 15),
        ]
    _anonymous_ = ("bits",)
    _fields_ = [
        ("bits", _Bits),
        ("VALUE", c_int),
    ]

class D128STATE(Structure):
    _fields_ = [
        ("CONTROL", CONTROLFLAGS),
        ("DEMAND", c_int),
        ("WIDTH", c_int),
        ("RECOVERY", c_int),
        ("DWELL", c_int),
        ("CPULSE", c_uint),
        ("COOC", c_uint),
        ("CTOOFAST", c_uint),
        ("FSTATE", STATEFLAGS),
    ]

class D128DEVICESTATE(Structure):
    _fields_ = [
        ("D128_DeviceID", c_int),
        ("D128_VersionID", c_int),
        ("D128_Error", c_int),
        ("D128_State", D128STATE),
    ]

class DEVHDR(Structure):
    _fields_ = [
        ("DeviceCount", c_int),
    ]

class D128(Structure):
    _fields_ = [
        ("Header", DEVHDR),
        ("State", D128DEVICESTATE),
    ]

# ------------------------------------------------------------------------------
# Declare DLL API function and associated parameters
protoDGD128_Initialise = WINFUNCTYPE (
    c_int,       #Function result
    c_void_p,    #Instance Reference
    c_void_p,    #Initialise Result
    c_int,       #Callback pointer (not used MUST be 0)
    c_int        #Callback parameters (not used MUST be 0)
    )

protoDGD128_Update = WINFUNCTYPE (
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

protoDGD128_Close = WINFUNCTYPE (
    c_int,       #Function result
    c_void_p,    #Instance Reference
    c_void_p,    #Close Result
    c_int,       #Callback pointer (not used MUST be 0)
    c_int        #Callback parameters (not used MUST be 0)
    )


paramsDGD128_Initialise = (1,"Reference",0),(1,"InitResult",0),(1,"CallbackProc",0),(1,"CallbackParam",0),
paramsDGD128_Update =  (1,"Reference",0),(1,"updateResult",0),(1,"NewState",0),(1,"cbNewState",0),(1,"CurrentState",0),(1,"cbCurrentState",0),(1,"CallbackProc",0),(1,"CallbackParam",0),
paramsDGD128_Close =  (1,"Reference",0),(1,"CloseResult",0),(1,"CallbackProc",0),(1,"CallbackParam",0),


DGD128_Initialise = protoDGD128_Initialise(("DGD128_Initialise",hDGD128Api), paramsDGD128_Initialise)
DGD128_Update = protoDGD128_Update(("DGD128_Update",hDGD128Api), paramsDGD128_Update)
DGD128_Close = protoDGD128_Close(("DGD128_Close",hDGD128Api), paramsDGD128_Close)

# ------------------------------------------------------------------------------
# Declare DS8R class

class DS8RController:
    def __init__(self):
        self.apiRef = c_int(0)          # Session reference
        self.retError = c_int(0)         # Initialization error
        self.retAPIError = c_int(0)      # General API error code
        self.closeResult = c_int(0)   

        self.DS8RMode = {
            'Mono-phasic': 1,
            'Bi-phasic': 2,
            'NoChange': 7
        }

        self.DS8RPol = {
            'Positive': 1,
            'Negative': 2,
            'Alternating': 3,
            'NoChange': 7
        }

        self.DS8RSrc = {
            'Internal': 1,   # (front panel)
            'External': 2,   # (rear panel BNC analog input)
            'NoChange': 7
        }

        self.DS8REnabled = {
            True: 1,
            False: 0
        }

    def Initialise(self):
        '''
        Must be the first function called to initialise the DS8R stack and return an
        instance reference.
        '''        
        self.apiRef = c_int(0)
        self.retAPIError = c_int(0)
        return DGD128_Initialise(byref(self.apiRef), byref(self.retAPIError), 0,0)
        
    def Close(self):
        '''
        Close and free all resources associated with the instance reference (apiRef).
        Called once DS8R has been finished with. It is advisable to hold on to the
        refernce until the end of the program
        '''
        self.closeResult = c_int(0)
        DGD128_Close(byref(self.apiRef), byref(self.closeResult), 0,0)
        
    def UpdateGet(self, STATE):
        '''
        Fetch the current state associated with the supplied instance reference.
        '''         
        self.retAPIError = c_int(0)  
        _STATE = D128()
        _cbSTATE = c_int(getsizeof(_STATE))
        DGD128_Update(self.apiRef, byref(self.retAPIError), 0, 0, byref(_STATE), byref(_cbSTATE), 0,0)
        STATE.Header = _STATE.Header
        STATE.State = _STATE.State
    
    def UpdateSet(self, STATE):
        '''
        Takes an object of type DS8R and updates the connected device to match the state
        '''
        self.retAPIError = c_int(0)  
        _STATE = D128()
        _cbSTATE = c_int(getsizeof(_STATE))
        _STATE.Header = STATE.Header
        _STATE.State = STATE.State
        DGD128_Update(self.apiRef, byref(self.retAPIError), byref(_STATE), _cbSTATE, byref(STATE), byref(_cbSTATE), 0,0)

    def Mode(self, mode_str):
        '''
        Set the mode Mono-phasic or Bi-phasic
        Args:
            mode (string): from self.DS8RMode typedef
        '''
        if mode_str in self.DS8RMode:
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.CONTROL.MODE = self.DS8RMode[mode_str]
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Mode argument invalid: {mode_str}')

    def Polarity(self, pol_str):
        '''
        Set the pulse polarity.
        Args:
            pol_str (string): from self.DS8RPol typedef
        '''
        if pol_str in self.DS8RPol:
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.CONTROL.POLARITY = self.DS8RPol[pol_str]
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Polarity argument invalid: {pol_str}')

    def Source(self, src_str):
        '''
        Set the source for the stimulus demand: USB or analog input.
        Args:
            src_str (string): from self.DS8RSrc typedef
        '''
        if src_str in self.DS8RSrc:
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.CONTROL.SOURCE = self.DS8RSrc[src_str]
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Source argument invalid: {src_str}')

    def Demand(self, value):
        '''
        Set amplitude
        Args:
            value (float): acceptable amplitude in [0-1000] mA with one decimal precision
        '''
        if 0 <= value <= 1000:
            value = round(value, 1)
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.DEMAND = int(value * 10) # function takes (mA * 10)
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Amplitude argument out of range')

    def Pulsewidth(self, value):
        '''
        Set pulsewidth. width of the first square in case of bi-phasic
        Args:
            value (int): acceptable pulsewidth in [50-2000] us 
        '''
        if 50 <= value <= 2000:
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.WIDTH = int(value)
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Pulsewidth argument out of range')

    def Dwell(self, value):
        '''
        Set inter-pulse width. Controls the period between the end of the first square and the start of the recovery square when BI-PHASIC mode is enabled.
        Args:
            value (int): acceptable interpulse width in [1-990] us 
        '''
        if 1 <= value <= 990 and (value == 1 or value % 10 == 0):
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.DWELL = int(value)
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Interpulse argument invalid')

    def Recovery(self, value):
        '''
        Controls the recovery pulse duration when the BI-PHASIC mode is selected. The value represents the percentage 
        Amplitude the recovery pulse will have. The recovery pulse duration is automatically adjusted to ensure the 
        pulse energy is the same as the stimulus pulse.
        Args:
            value (int): acceptable recovery phase value in [10-100] %
        '''
        if 10 <= value <= 100:
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.RECOVERY = int(value)
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Recovery argument out of range')

    def Enable(self, enabled):
        '''
        Control of output enable state.
        Args:
            enabled (bool)
        '''
        if isinstance(enabled, bool):
            STATE = D128()
            self.UpdateGet(STATE)
            STATE.State.D128_State.CONTROL.ENABLE = self.DS8REnabled[enabled]
            self.UpdateSet(STATE)
        else:
            print(f'ERROR! Enable argument invalid: {enabled}')
    
    def Trigger(self):
        '''
        Triggers one time. TRIGGER is 0 in idle. Setting it to 1 triggers. After triggering it will be set back to zero automatically by the device 
        REMARK: Max trigger at 10Hz using USB, otherwise can have bugs
        '''
        STATE = D128()
        self.UpdateGet(STATE)
        STATE.State.D128_State.CONTROL.TRIGGER = 1
        self.UpdateSet(STATE)

    def Status(self):
        '''
        Get current state of device
        '''
        STATE = D128()
        self.UpdateGet(STATE)
        return {
                'mode': STATE.State.D128_State.CONTROL.MODE,
                'polarity': STATE.State.D128_State.CONTROL.POLARITY,
                'source': STATE.State.D128_State.CONTROL.SOURCE,
                'demand': STATE.State.D128_State.DEMAND,
                'pulsewidth': STATE.State.D128_State.WIDTH,
                'dwell': STATE.State.D128_State.DWELL,
                'recovery': STATE.State.D128_State.RECOVERY,
                'enabled': STATE.State.D128_State.CONTROL.ENABLE
            }

    def PrintState(self):
        '''
        Print the current content of the DS8R STATE
        '''
        STATE = D128()
        self.UpdateGet(STATE)
        print(
            {
                'mode': STATE.State.D128_State.CONTROL.MODE,
                'polarity': STATE.State.D128_State.CONTROL.POLARITY,
                'source': STATE.State.D128_State.CONTROL.SOURCE,
                'demand': STATE.State.D128_State.DEMAND,
                'pulsewidth': STATE.State.D128_State.WIDTH,
                'dwell': STATE.State.D128_State.DWELL,
                'recovery': STATE.State.D128_State.RECOVERY,
                'enabled': STATE.State.D128_State.CONTROL.ENABLE
            }
        )

    def Cmd(self, command, *args):
        '''
        This is just a dispatcher function that provides a different format for calling the previous functions:
        Mode, Polarity, Source, Demand, Pulsewidth, Dwell, Recovery
        Args:
            command (string): different commands
            *args: different possible values depending on the command
        '''
        if command.lower() == 'mode':
            if len(args) == 1:
                mode_str = args[0]
                self.Mode(mode_str)
            else:
                print('Unexpected number of arguments for mode command')
                print('\tmode - ' + ', '.join(self.DS8RMode.keys()))

        elif command.lower() == 'polarity':
            if len(args) == 1:
                pol_str = args[0]
                self.Polarity(pol_str)
            else:
                print('Unexpected number of arguments for polarity command')
                print('\tpolarity - ' + ', '.join(self.DS8RPol.keys()))

        elif command.lower() == 'source':
            if len(args) == 1:
                src_str = args[0]
                self.Source(src_str)
            else:
                print('Unexpected number of arguments for source command')
                print('\tsource - ' + ', '.join(self.DS8RSrc.keys()))

        elif command.lower() == 'demand':
            if len(args) == 1:
                pulse_amp = args[0]
                self.Demand(pulse_amp)
            else:
                print('Unexpected number of arguments for demand command')
                print('\tdemand - float value between 0 and 1000. max one decimal point') 

        elif command.lower() == 'pulsewidth':
            if len(args) == 1:
                pulse_width = args[0]
                self.Pulsewidth(pulse_width)
            else:
                print('Unexpected number of arguments for pulsewidth command')
                print('\tpulsewidth - integer value between 50 and 2000')

        elif command.lower() == 'dwell':
            if len(args) == 1:
                inter_pulse = args[0]
                self.Dwell(inter_pulse)
            else:
                print('Unexpected number of arguments for dwell command')
                print('\tInterpulse delay - integer value between 1 and 990')

        elif command.lower() == 'recovery':
            if len(args) == 1:
                rec_percentage = args[0]
                self.Recovery(rec_percentage)
            else:
                print('Unexpected number of arguments for recovery command')
                print('\trecovery - integer value between 10 and 100')
        else:
            print('ERROR! Unrecognized command for the DS8R')


if __name__ == "__main__":
    '''
    Note: Every communication opened with Initialise must be closed afterwards, otherwise get memory handeling problems
    '''
    ds8r = DS8RController()
    ds8r.Initialise()
    ds8r.Mode('Bi-phasic')
    ds8r.Polarity('Negative')
    ds8r.Source('Internal')
    ds8r.Cmd('demand', 2)
    ds8r.Cmd('pulsewidth', 50)
    ds8r.Cmd('dwell', 10)
    ds8r.Cmd('recovery', 100)
    ds8r.Enable(True)
    ds8r.Trigger()
    ds8r.Enable(False)
    ds8r.PrintState()
    ds8r.Close()
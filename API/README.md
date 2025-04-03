The original DLL is used to create these API functions that can be used in the future.

## D188 Controller

| Command   | Parameter |Description                              |
| --------  | ------------ | ---------------------------------------- |
| `Initialise` | None | Must be the first function called to initialise the D188 stack and return an instance reference. |
| `SetChannel` | channel | Set which channel is active: (int) in [0-8] with zero equivalent to all channels open. |
| `SetMode` | mode | Set which controll mode is used for the selector: (string) 'OFF', 'USB', '8TTL' or '4TTL' |
| `SetIndicator` | state | Set the LED indicators as activated/disactivated: (string) 'ON' or 'OFF'. |
| `SetDelay` | delay | Set the The Delay/De-bounce setting. delay (float): between 0.1-1000 milliseconds. |
| `PrintState` | None | Print the current content of the D188 STATE. |
| `Close` | None | Close and free all resources associated with the instance reference (apiRef). Called once D188 has been finished with. |

## DS8R Controller
| Command   | Parameter |Description                              |
| --------  | ------------ | ---------------------------------------- |
| `Initialise` | None | Must be the first function called to initialise the DS8R stack and return an instance reference. |
| `Mode` | mode | Set the mode: (string) 'Mono-phasic' or 'Bi-phasic'. |
| `Polarity` | polarity | Set the pulse polarity: (string): 'Positive', 'Negative', 'Alternating' |
| `Source` | source | Set the source for the stimulus amplitude: (string) 'Internal' for USB and front pannel or 'External' for analog input in the back of the device. |
| `Demand` | amplitude | Set amplitude. (float): acceptable amplitude in [0-1000] mA with one decimal precision |
| `Pulsewidth` | width | Set pulsewidth. Width of the first square in case of bi-phasic. (int): acceptable pulsewidth in [50-2000] us. |
| `Dwell` | interpulse | Set inter-pulse width. Controls the period between the end of the first square and the start of the recovery square when BI-PHASIC mode is enabled. (int): acceptable interpulse width in [1-990] us with increments of 10us. |
| `Recovery` | percentage | Controls the recovery pulse duration when the BI-PHASIC mode is selected. The value represents the percentage amplitude the recovery pulse will have compared to the first pulse. The recovery pulse duration is automatically adjusted to ensure the pulse energy is the same as the stimulus pulse. |
| `Enable` | enabled | Control of output enable state. (bool) |
| `Trigger` | None | Triggers one time. Max trigger at 10Hz using USB, otherwise can have bugs. |
| `Status` | None | Get current state of device |
| `PrintState` | None | Print the current content of the DS8R STATE |
| `Cmd` | command, *args | This is just a dispatcher function that provides a different format for calling the previous functions: command takes a string of the function name (string): 'Mode', 'Polarity', 'Source', 'Demand', 'Pulsewidth', 'Dwell', 'Recovery' and *args value respects th previous commands requirements. |
| `Close` | None | Close and free all resources associated with the instance reference (apiRef). Called once DS8R has been finished with. |
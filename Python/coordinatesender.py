import serial
import time

'''
    Class Name: coordinateSender
    - Helper class for GUI.py which sends a list of coordinates via pyserial.
'''
class coordinateSender:
    '''
        Function Name: __init__
        Inputs: self, port
    '''
    def __init__(self, port):
        self.CLEAR_CODE = 0 # Code corresponding to CLEAR function on the Arduino.
        self.ON_CODE = 1 # Code corresponding to LED_ON function on the Arduino.
        self.OFF_CODE = 2 # Code corresponding to LED_OFF function on the Arduino.
        self.DELIMITER = ' ' # Delimiter on the Arduino.
        self.serial = serial.Serial(port, 9600) # Begins a serial correction on 'port' at a baud rate of 9600.
        time.sleep(5) # Wait for Serial to initialise.

    '''
        Function Name: sendCoords
        Inputs: coords
                - coords is a list of [X, Y] ordered pairs.
        Example Call:
            To Send a LED_ON command to a list of coordinates C
                self.sendCoords(C)
    '''
    def sendCoords(self, coords):

        # Clear the LED display
        self.serial.write((str(self.CLEAR_CODE) + self.DELIMITER).encode());
        time.sleep(.1) # Wait for arduino.

        # Loop through the coordinates
        for coord in coords:
            # Compose the message and send using serial.write
            coordString = str(self.ON_CODE) + self.DELIMITER + str(coord[0]) + self.DELIMITER + str(coord[1]) + self.DELIMITER
            self.serial.write(coordString.encode())
            time.sleep(.1) # A PC is just so much faster than the Arduino isn't it?

        # Print messages sent by the Arduino.
        while self.serial.in_waiting:
            print(self.serial.readline())

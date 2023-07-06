# This script is used for the Black Screen Test SWDEV-406688
# NOTE: This script runs locally on the TARGET machine using a .bat file tha is called by the HOST machine through PS Exec

from serial.tools.list_ports import comports
from statistics import mean
import serial
import sys

BAUDRATE_MCU = 115200 # Baudrate used to sync between the light sensor and the Arduino device
TIMEOUT_SEC = 2
LIGHT_SENSOR_SCREEN_ON_THRESHOLD_VALUE = 15 # Lux threshold to determine whether screen is lit/not lit

EXIT_SCREEN_LIT                     = 0 # returned if screen is lit (lux value is > 45)
EXIT_SCREEN_NOT_LIT                 = 2 # returned if screen is not lit (lux value is < 45)
EXIT_HW_NOT_FOUND_MCU               = 3 # returned if Arduino was not found
EXIT_HW_NOT_FOUND_SENSOR            = 4 # returned if sensor was not found

def light_up_check():
    
    fail = True

    #Find which COM port is connected to Arduino
    for port in comports():
        port_str = str(port)
        if (port_str.find("Arduino Uno") != -1):
            arduino_port = port_str[0:4]
            print("Arduino is connected to ",arduino_port)
            fail = False
            break

    if (fail == True):
        print("Arduino not found! Check connection between host system and Arduino")
        return sys.exit(EXIT_HW_NOT_FOUND_MCU)

    serialport = serial.Serial(arduino_port, baudrate=BAUDRATE_MCU, timeout=TIMEOUT_SEC)

    # Checks if light sensor is connected to the arduino or not
    for i in range(0,10): 
        arduinodata = serialport.readline().decode('ascii')
        print(arduinodata) # Prints Arduino data output to terminal
        if (arduinodata.find("Sensor not found") != -1):
            print("Error: Sensor Not Found! Check connection between Arduino and light sensor")
            return sys.exit(EXIT_HW_NOT_FOUND_SENSOR)

    # Checks if screen is lit or not through lux value returned from the light sensor
    lux_list = []
    for i in range(0, 5):
        arduinodata = serialport.readline().decode('ascii')
        lux_list.append(float(arduinodata))

    lux_average = mean(lux_list) # Gets average of lux value of lux data points

    if (lux_average < LIGHT_SENSOR_SCREEN_ON_THRESHOLD_VALUE):
        print("Lux value is = ", lux_average, " Screen did not light up! *** FAIL ***")
        fail = True
        return sys.exit(EXIT_SCREEN_NOT_LIT)
    else:
        print("Lux value is = ", lux_average, " Screen is lit. *** PASS ***")
        fail = False
        return sys.exit(EXIT_SCREEN_LIT)    

def main():
    return light_up_check()

if __name__ == '__main__':
    print("***** Checking for light up on screen. *****")  
    main()
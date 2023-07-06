### [PURPOSE] ###
   Remotely check if a screen or any surface is lit-up using an Arduino kit + VEML7700 light sensor

### [METHOD] ###
   Using an Arduino board + Adafruit veml7700 light sensor kit, the light sensor is mounted to the screen's bottom portion where windows taskbar is to measure the lux value of the screen surface. 
   If the value is higher than the assigned threshold, the screen is lit, else it is not lit.

### [PROCESS] ###
  > Arduino kit + sensor are taped to the taskbar location (bottom of screen) of the DUT (device under test)
  > blackScreenTest.py and blackScreenTest.bat are copied to a directory on the DUT
  > blackScreenTest.bat is ran (either remotely or locally) to run the .py script and read the Arduino's output
  > User gets results indicating whether the screen is lit, not lit, arduino not detected, sensor not detected, or the blackScreenTest.py script is failing to run

### [FLASHING ARDUINO KIT WITH CORRECT BINARIES] ###
  To flash the arduino board we use Arduino IDE and run "veml7700_test.ino" located in dal repo under the following path: 
  AMD-Radeon-Driver/dal/test/usb4_automation_test_suite/dpia_usb4_automation_tool_v3.1/scripts/blackScreenTest(SWDEV-406688)/veml7700_test/veml7700_test.ino

### [PROCESS OF FLASHING ARDUINO KIT] ###
  1- Install Arduino IDE on your dev machine
  2- Import Adafruit_VEML7700 library from Arduino IDE [Sketch -> Include Library -> Manage Libraries -> Search for 'Adafruit VEML7700' -> Install and include the library]
  3- Upload to Arduino 
  4- Match BAUD rate w/ Serial.begin(baudRate)
  5- Enable Serial Monitor (to see lux value output)

### [WHEN TO FLASH ARDUINO KIT] ###
  > If using a new Arduino or an Arduino that was used for a different application
  > If Arduino is not detected by the machine and/or the Arduino is acting abnormally
  > If the Arduino loses power
  > If unsure of any of the above cases, reflash the Arduino just to be safe
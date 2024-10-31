# CAN Network Parser

## Description
This Controller Area Network (CAN) Parser is reading CAN networks built for FPU's Solar Car.  
It reads the packets sent by the components on board the vehicle and converts it to readable format.  
This program currently populates with a Tkinter GUI that shows data  
on screen for the user to see while driving.  


This software uses a Raspberry Pi connected by a PCAN adapter and an Arduino  
connected via USB to read and display data. The Raspberry Pi handles the  
CAN network and GUI display. The Arduino takes in a pulse from the  
Electronic Speed Controller (ESC) and calculates speed. Then its passed  
over USB connection to the Raspberry Pi and displayed on the GUI.

## Components and CAN ID
### **Prohelion BMU:**  
- CMU Base Id's: **0x301 <= SENSOR <= 0x3F3**
- BMU Heartbeat Sensor: **0x300**
- Pack State of Charge (SoC): **0x3F4**
- Pack Balance SoC: **0x3F5**
- Charger Control Info: **0x3F6**
- Precharge Status: **0x3F7**
- Min/Max Cell Voltage: **0x3F8**
- Min/Max Cell Temp: **0x3F9**
- Battery Pack Info: **0x3FA**
- Battery Pack Status: **0x3FB**
- Battery Pack Fan Status: **0x3FC**
- Battery Pack Extended Info: **0x3FD**
----------------------------------
### **Solar Array:**  
- MPPT1 Input: **0x600**
- MPPT1 Output: **0x601**
- MPPT1 Temp: **0x602**
- MPPT1 Aux Power: **0x603**
- MPPT1 Limits: **0x604**
- MPPT1 Status: **0x605**
- MPPT1 Power Connector: **0x606**
- MPPT1 Mode (send): **0x608**
- MPPT1 Max Output Voltage: **0x60A**
- MPPT1 Max Input Current: **0x60B**
----------------------------------
- MPPT2 Input: **0x610**
- MPPT2 Output: **0x611**
- MPPT2 Temp: **0x612**
- MPPT2 Aux Power: **0x613**
- MPPT2 Limits: **0x614**
- MPPT2 Status: **0x615**
- MPPT2 Power Connector: **0x616**
- MPPT2 Mode (send): **0x618**
- MPPT2 Max Output Voltage: **0x61A**
- MPPT2 Max Input Current: **0x61B**

## GUI
The GUI currently shows on screen:  
- Speed (Mph and Rpm)
- State of Charge (SoC)
- MPPT1 Input Voltage
- MPPT1 Input Current
- MPPT2 Input Voltage
- MPPT2 Input Current

## Installation/Setup
Installation is intended to work on ***Raspberry Pi OS***  
Copy all files into local directory: `git clone https://github.com/PheonixRacingUnofficial/CANDataParser.git`  


Create Virtual Environment: `python3 -m venv venv`  
Activate Virtual Environment: `source venv/bin/activate`  


Install the requirements: `pip install -r requirements.txt`  
***Bug: Need to individually install certain packages***  
Python Can: `pip install python-can`  
Serial: `pip install serial`  


Install **Tkinter:** `sudo apt install python3-tk`  

## How to Use
To see most utility: `python3 main.py --help`  
***CAN network setup*** `python3 main.py --setup`  
***Check Status*** `python3 main.py --status`  


Primary use: `python3 main.py --serial PORT`  


Replace "PORT" with the port that the CAN line is connected to  
Ex: ACM0 *This is the port used with our specific setup*  


To log the output: `python3 main.py --serial PORT --log`  
or: `python3 main.py --serial PORT > log.txt`  
Both commands simply log the would be terminal output  
For more output: `python3 main.py --serial PORT --debug  

import argparse
import os
import platform

import serial

import Parser
import can_receiver


def main():
    arg_parse = argparse.ArgumentParser(description="Process, log, and display CAN data")
    arg_parse.add_argument("--manual", action="store_true", help="Manual CAN line input on command line")
    arg_parse.add_argument("--status", action="store_true", help="Determine pCAN connection status")
    arg_parse.add_argument("--file", action="store_true", help="Read CAN data from file")
    arg_parse.add_argument("--debug" , action="store_true", help="Debug mode for CAN data")
    arg_parse.add_argument("--log", action="store_true", help="Logs data in log.txt is local directory")
    arg_parse.add_argument("--setup", action="store_true", help="Sets CAN0 interface to active")
    arg_parse.add_argument("--nogui", action="store_true", help="Run without GUI")
    arg_parse.add_argument("--serial", action="store_true", help="Run with serial connection")

    args = arg_parse.parse_args()

    is_debug: bool = args.debug
    is_log: bool = args.log

    if args.setup:
            # Automatically set CAN0 port to activate for data transmission
            try:
                os.system("sudo ip link set can0 up type can bitrate 500000")
            # Interesting bug where it makes it through even without sudo privilages
            except Exception as e:
                print(f"MAIN::can_set_up::error {e}")

    if not args.nogui:
        ...

    if args.serial:
        try:
            ser = get_serial_port()
            print(f"Connected to serial port: {ser.port}")
            while True:
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode('utf-8').strip()
                    except UnicodeDecodeError:
                        print("Error: Could not decode the data")
                    try:

                        time_value, voltage_value = map(float, line.split(','))
                        if voltage_value < 1:
                            voltage_value = 0.0
                        if voltage_value > 4:
                            voltage_value = 5.0
                    except ValueError:
                        print(f"Invalid data format: {line}")
                        time_value, voltage_value = 0, 0

                    print(f"Time: {time_value}, Voltage: {voltage_value}")

                    with open('serial_data.txt', 'a') as file:
                        file.write(f"{time_value}, {voltage_value}\n")


        except Exception as e:
            print(f"Error: Could not connect to serial port: {e}")

    if args.manual:
        manual_loop(is_debug)
    if args.status:
        if not can_receiver.get_status():
            return
    elif args.file:
        run_file(is_debug)
    else:
        # Initialize Socket CAN to read from the correct bus
        bus = can_receiver.get_data_bus()
        # Continuously dump the data into parser
        while True:
            # retrieve data from the CAN network
            message = can_receiver.get_can_line(bus)
            # print("TYPE: ", type(message), ' ', str(message))
            # failed to receive message break from loop
            if message == None:
                break
            # print and log the data
            if is_log:
                file = open("log.txt", "a")
                file.write(str(message) + '\n')
            # message = can_receiver.clean_message(message)
            Parser.parse_can_line(message, is_debug)

def get_serial_port():
    """Detect OS and bind the corresponding serial port."""
    os_name = platform.system()
    if os_name == "Linux":
        return serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    elif os_name == "Windows":
        return serial.Serial('COM4', 115200, timeout=1)  # Adjust the COM port as needed
    else:
        raise OSError(f"Unsupported OS: {os_name}")

def manual_loop(is_debug: bool) -> None:
    """ Manual input loop for CAN data. """
    running: bool = True
    while running:
        data: str = input("Enter CAN data line: ")
        Parser.parse_can_line(data, is_debug)
        running = input("Continue? (y/n) ") == 'y'

def run_file(is_debug: bool) -> None:
    """ Read CAN data from a file and process it. """
    input_file_path = input("Enter the input file path: ")
    output_file_path = input("Enter the output file path: ")
    with open(output_file_path, 'w') as file_handle:
        with open(input_file_path, 'r') as file:
            for line in file:
                file_handle.write(Parser.parse_can_line(line, is_debug))

if __name__ == '__main__':
    main()


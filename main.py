import argparse
import os
import platform
import queue
import threading

import serial

import Parser
import can_receiver
import gui

data_queue = queue.Queue()


def main():
    arg_parse = argparse.ArgumentParser(description="Process, log, and display CAN data")
    arg_parse.add_argument("--manual", action="store_true", help="Manual CAN line input on command line")
    arg_parse.add_argument("--status", action="store_true", help="Determine pCAN connection status")
    arg_parse.add_argument("--file", action="store_true", help="Read CAN data from file")
    arg_parse.add_argument("--debug" , action="store_true", help="Debug mode for CAN data")
    arg_parse.add_argument("--log", action="store_true", help="Logs data in log.txt is local directory")
    arg_parse.add_argument("--setup", action="store_true", help="Sets CAN0 interface to active")
    arg_parse.add_argument("--nogui", action="store_true", help="Run without GUI")
    arg_parse.add_argument("--serial", type=str, help="Run with serial connection")

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
        gui_thread = threading.Thread(target=gui.start_gui, args=(data_queue,), daemon=True)
        gui_thread.start()
    if args.serial:
        serial_thread = threading.Thread(target=run_serial, args=(is_debug, is_log, args.serial), daemon=True)
        serial_thread.start()
    if args.manual:
        run_manual(is_debug, is_log)
    if args.status:
        if not can_receiver.get_status():
            return
    elif args.file:
        run_file(is_debug, is_log)
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
            Parser.parse_can_line(message, is_debug, is_log)

def get_serial_port(port: str) -> serial.Serial:
    """Detect OS and bind the corresponding serial port."""
    os_name = platform.system()
    if os_name == "Linux":
        return serial.Serial(f'/dev/tty{port}', 115200, timeout=1)
    elif os_name == "Windows":
        return serial.Serial(port, 115200, timeout=1)
    else:
        raise OSError(f"Unsupported OS: {os_name}")

def run_manual(is_debug: bool, is_log: bool) -> None:
    """ Manual input loop for CAN data. """
    running: bool = True
    while running:
        data: str = input("Enter CAN data line: ")
        return_data = Parser.parse_can_line(data, is_debug, is_log)
        if type(return_data) == dict:
            data_queue.put(return_data)
        running = input("Continue? (y/n) ") == 'y'

def run_file(is_debug: bool, is_log: bool) -> None:
    """ Read CAN data from a file and process it. """
    input_file_path = input("Enter the input file path: ")
    output_file_path = input("Enter the output file path: ")
    with open(output_file_path, 'w') as file_handle:
        with open(input_file_path, 'r') as file:
            for line in file:
                return_data = Parser.parse_can_line(line, is_debug, is_log)
                if type(return_data) == dict:
                    data_queue.put(return_data)
                file_handle.write(return_data)

def run_serial(is_debug: bool, is_log: bool, port: str) -> None:
    try:
        ser = get_serial_port(port)
        print(f"Connected to serial port: {ser.port}")
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()
                except UnicodeDecodeError:
                    print("Error: Could not decode the data")
                    line = ""
                try:

                    mph = line.split(' ')[1]
                except ValueError:
                    print(f"Invalid data format: {line}")
                    mph = 0
                data_queue.put({'speed': f"Speed: {mph} MPH"})
                if is_debug:
                    print(f"MPH: {mph}")
                if is_log:
                    with open('serial_data.txt', 'a') as file:
                        file.write(f"MPH: {mph}\n")


    except Exception as e:
        print(f"Error: Could not connect to serial port: {e}")

if __name__ == '__main__':
    main()


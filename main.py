import can_receiver
import Parser
import argparse
import os

def main():
    # User inputs defined parameters to get to desired mode: auto/manual
    arg_parse = argparse.ArgumentParser(description="Process, log, and display CAN data")
    arg_parse.add_argument("--manual", action="store_true", help="Manual CAN line input on command line")
    arg_parse.add_argument("--status", action="store_true", help="Determine pCAN connection status")
    arg_parse.add_argument("--file", action="store_true", help="Read CAN data from file")
    arg_parse.add_argument("--debug" , action="store_true", help="Debug mode for CAN data")
    arg_parse.add_argument("--log", action="store_true", help="Logs data in log.txt is local directory")
    arg_parse.add_argument("--setup", action="store_true", help="Sets CAN0 interface to active")
    # Determine what the users arguments are
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

    # Manual User Input for CAN data
    if args.manual:
        running: bool = True
        while running:
            data: str = input("Enter CAN data line: ")
            print(Parser.parse_can_line(data, is_debug))
            running = input("Continue? (y/n) ") == 'y'
    # Determine CAN network status
    if args.status:
        if not can_receiver.get_status():
            return
    # Automatically take in process and display data in the terminal
    elif args.file:
        # Get the input file path
        input_file_path = input("Enter the input file path: ")
        # Get the output file path
        output_file_path = input("Enter the output file path: ")
        with open(output_file_path, 'w') as file_handle:
            with open(input_file_path, 'r') as file:
                for line in file:
                    file_handle.write(Parser.parse_can_line(line, is_debug))
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
            print(Parser.parse_can_line(message, is_debug))

if __name__ == '__main__':
    main()

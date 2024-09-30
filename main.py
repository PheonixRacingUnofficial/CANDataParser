import can_receiver
import Parser
import argparse
import os

def main():
	# Automatically set CAN0 port to activate for data transmission
	try:
		os.system("sudo ip link set can0 up type can bitrate 500000")
		# Interesting bug where it makes it through even without sudo privilages
		print("CAN0 port is active")
	except Exception as e:
		print(f"MAIN::can_set_up::error {e}")

	# User inputs defined parameters to get to desired mode: auto/manual
	arg_parse = argparse.ArgumentParser(description="Process, log, and display CAN data")
	arg_parse.add_argument("--manual", action="store_true", help="Manual CAN line input on command line")
	arg_parse.add_argument("--status", action="store_true", help="Determine pCAN connection status")
	arg_parse.add_argument("--file", action="store_true", help="Read CAN data from file")

	# Determine what the users arguments are
	args = arg_parse.parse_args()

	# Manual User Input for CAN data
	if args.manual:
		running: bool = True
		while running:
			data: str = input("Enter CAN data line: ")
			print(Parser.parse_can_line(data, True))
			running = input("Continue? (y/n) ") == 'y'
	# Determine CAN network status
	elif args.status:
		print(f"Found CAN network? {can_receiver.get_status()}")
	# Automatically take in process and display data in the terminal
	elif args.file:
		# Get the input file path
		input_file_path = input("Enter the input file path: ")
		# Get the output file path
		output_file_path = input("Enter the output file path: ")
		with open(output_file_path, 'w') as file_handle:
			with open(input_file_path, 'r') as file:
				for line in file:
					file_handle.write(Parser.parse_can_line(line, False) + '\n')
	else:
		# Initialize Socket CAN to read from the correct bus
		bus = can_receiver.get_data_bus()
		# Continuously dump the data into parser
		while True:
			# retrieve data from the CAN network
			message = can_receiver.get_can_line(bus)
			# failed to receive message break from loop
			if message == None:
				break
			# print and log the data
			message = can_receiver.clean_data(message)
			print(Parser.parse_can_line(message, False))

if __name__ == '__main__':
	main()

import can_receiver
import Parser
import argparse

def main():
	# User inputs defined parameters to get to desired mode: auto/manual
	arg_parse = argparse.ArgumentParser(description="Process, log, and display CAN data")
	arg_parse.add_argument("--manual", action="store_true", help="Manual CAN line input on command line")
	arg_parse.add_argument("--file", action="store_true", help="Read CAN data from file")

	# Determine what the users arguments are
	args = arg_parse.parse_args()

	if args.manual:
		running: bool = True
		while running:
			data: str = input("Enter CAN data line: ")
			print(Parser.parse_can_line(data, True))
			running = input("Continue? (y/n) ") == 'y'
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
			if message == "0":
				break
			# print and log the data
			print(Parser.parse_can_line(message, False))
	

if __name__ == '__main__':
	main()

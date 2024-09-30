import can_receiver
import Parser
import argparse

def main():
	# User inputs defined parameters to get to desired mode: auto/manual
	arg_parse = argparse.ArgumentParser(description="Process, log, and display CAN data")
	arg_parse.add_argument("--manual", action="store_true", help="Manual CAN line input on command line")
	arg_parse.add_argument("--status", action="store_true", help="Determine pCAN connection status")
	# Determine what the users arguments are --manual or nothing
	args = arg_parse.parse_args()

	if args.manual:
		running: bool = True
		while running:
			data: str = input("Enter CAN data line: ")
			print(Parser.parse_can_line(data))
			running = input("Continue? (y/n) ") == 'y'
	if args.status:
		print(f"Found CAN network? {can_receiver.get_status()}")
	else:
		# Initialize Socket CAN to read from the correct bus
		bus = can_receiver.get_data_bus()
		# Continuously dump the data into parser
		while (True):
			# Should attempt to connect to the CAN network
			if bus == None:
				break
			# retrieve data from the CAN network
			message = can_receiver.get_can_line(bus)
			# failed to receive message break from loop
			if message == None:
				break
			# print and log the data
			print(Parser.parse_can_line(message))
	

if __name__ == '__main__':
	main()

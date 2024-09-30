import can
import re

def get_data_bus():
	try:
		# Get and bind the CAN network on the usb port
		bus = can.interface.Bus(channel='can0', bustype='socketcan')
		return bus
	except OSError as e:
		if e.errno != 19:
			print(f"CAN_RECEIVER::get_data_bus::Unknown error: {e.errno}")
		print("CAN_RECEIVER::get_data_bus::can network not found")
	except Exception as e:
		print(f"CAN_RECEIVER::get_data_bus::unknown exception: {e}")
	return None

# Get and return a CAN message
def get_can_line(bus):
	try:
		# Message format is different from can-utils candump can0 (the log file we tested on)
		return bus.recv(timeout=1.0)
	except AttributeError as e:
		print(f"Error: {e}")
		return None

# Simply detect if the network has been found and has been bound to an address
def get_status():
	try:
		bus = can.Bus(channel='can0', interface='socketcan')
		print("First")
		return True
	except Exception as e:
		print("CAN_RECEIVER::get_status::CAN network not found")
	return False

# Clean the data given by python-can
def clean_message(message):
	# Extract information using regular expressions
	timestamp = re.search(r'Timestamp:\s*([\d.]+)', input_string).group(1)
	id_value = re.search(r'ID:\s*(\d+)', input_string).group(1)
	data = re.search(r'DL:\s*\d+\s*((?:[a-f0-9]{2}\s*)+)', input_string).group(1)
	channel = re.search(r'Channel:\s*(\w+)', input_string).group(1)

	# Format the output
	formatted_output = f"({timestamp}) {channel} {id_value}#{data.replace(' ', '')}"
	return formatted_output

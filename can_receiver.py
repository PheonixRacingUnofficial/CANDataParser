import can

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

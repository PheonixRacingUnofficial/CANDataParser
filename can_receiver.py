import can

def get_data_bus():
	try:
		bus = can.interface.Bus(channel='can0', bustype='socketcan')
		return bus
	except OSError as e:
		if e.errno != 19:
			print(f"CAN_RECEIVER::get_data_bus::Unknown error: {e.errno}")
		print("CAN_RECEIVER::get_data_bus::can network not found")
	except Exception as e:
		print(f"CAN_RECEIVER::get_data_bus::unknown exception: {e}")
	return None

def get_can_line(bus):
	try:
		return bus.recv()
	except AttributeError as e:
		print(f"Error: {e}")
		return None

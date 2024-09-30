import can

def get_data_bus():
	try:
		bus = can.Bus(channel='can0', interface='socketcan')
		return bus
	except OSError as e:
		if e.errno != 19:
			print(f"Unknown error: {e.errno}")
		return -1

def get_can_line(bus):
	try:
		return bus.recv()
	except AttributeError as e:
		print(f"Error: {e}")
		return "no data"

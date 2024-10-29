import struct

def hex_to_int8(hex_str):
    """ Convert a hex string to a signed 8-bit integer """
    return struct.unpack('>b', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_uint8(hex_str):
    """ Convert a hex string to an unsigned 8-bit integer """
    return struct.unpack('>B', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_int16(hex_str):
    """ Convert a hex string to a signed 16-bit integer """
    return struct.unpack('>h', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_uint16(hex_str):
    """ Convert a hex string to an unsigned 16-bit integer """
    return struct.unpack('>H', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_int32(hex_str):
    """ Convert a hex string to a signed 32-bit integer """
    return struct.unpack('>i', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_uint32(hex_str):
    """ Convert a hex string to an unsigned 32-bit integer """
    return struct.unpack('>I', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_float(hex_str):
    """ Convert a hex string to a 32-bit float """
    return struct.unpack('>f', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_bits(hex_str):
    """ Convert a hex string to its equivalent binary string """
    # convert a string of hex values to its equivalent binary string then fill in the missing 0s
    return bin(int(hex_inverter(hex_str), 16))[2:].zfill(len(hex_str) * 4)

def hex_inverter(hex_str: str) -> str:
    """ Invert the hex string by converting it into a list of 2 character strings, reversing the list, and joining it back together """
    hex_str = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    hex_str = hex_str[::-1]
    hex_str = "".join(hex_str)
    return hex_str
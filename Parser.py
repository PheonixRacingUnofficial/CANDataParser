import datetime
import re
import struct

def hex_to_int8(hex_str):
    return struct.unpack('>b', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_uint8(hex_str):
    return struct.unpack('>B', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_int16(hex_str):
    return struct.unpack('>h', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_uint16(hex_str):
    return struct.unpack('>H', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_int32(hex_str):
    return struct.unpack('>i', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_uint32(hex_str):
    return struct.unpack('>I', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_to_float(hex_str):
    return struct.unpack('>f', bytes.fromhex(hex_inverter(hex_str)))[0]

def hex_inverter(hex_str) -> str:
    """ Invert the hex string by converting it into a list of 2 character strings, reversing the list, and joining it back together """
    hex_str = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    hex_str = hex_str[::-1]
    hex_str = "".join(hex_str)
    return hex_str

def parse_cmu_sensor(sensor_id: int, sensor_data: str, time: str) -> str:
    base_id = 0x301
    sensor_index = (sensor_id - base_id) // 3 + 1  # Determine which sensor (e.g., 1, 2, 3...)

    # Determine which part of the CMU data this is (e.g., Serial & Temp, Cell Voltages 0-3, Cell Voltages 4-7)
    part = (sensor_id - base_id) % 3

    out = f"{time}CMU Sensor {sensor_index}; "

    if part == 0:  # Serial number and temperatures
        cmu_serial_number = hex_to_uint32(sensor_data[:8])
        cmu_pcb_temp = hex_to_int16(sensor_data[8:12]) / 10
        cmu_cell_temp = hex_to_int16(sensor_data[12:16]) / 10
        out += f"Serial Number: {cmu_serial_number}; PCB Temp: {cmu_pcb_temp}°C; Cell Temp: {cmu_cell_temp}°C"

    elif part == 1:  # Cell voltages 0-3
        c0_voltage = hex_to_int16(sensor_data[:4])
        c1_voltage = hex_to_int16(sensor_data[4:8])
        c2_voltage = hex_to_int16(sensor_data[8:12])
        c3_voltage = hex_to_int16(sensor_data[12:16])
        out += f"Cell 0 Voltage: {c0_voltage}mV; Cell 1 Voltage: {c1_voltage}mV; Cell 2 Voltage: {c2_voltage}mV; Cell 3 Voltage: {c3_voltage}mV"

    elif part == 2:  # Cell voltages 4-7
        c4_voltage = hex_to_int16(sensor_data[:4])
        c5_voltage = hex_to_int16(sensor_data[4:8])
        c6_voltage = hex_to_int16(sensor_data[8:12])
        c7_voltage = hex_to_int16(sensor_data[12:16])
        out += f"Cell 4 Voltage: {c4_voltage}mV; Cell 5 Voltage: {c5_voltage}mV; Cell 6 Voltage: {c6_voltage}mV; Cell 7 Voltage: {c7_voltage}mV"
    else:
        print("What happen:(?")
        return f"CMU Sensor {sensor_index} part {part} not recognized; Data: {sensor_data[:-1]}"

    return out

def parse_can_line(data: str, debug: bool) -> str:
    # Better error handling
    if data[0] == '(':
        # Normal CAN data, continue as normal
        if debug:
            print("This is a CAN log line")
        ...
    elif data[0] == ';':
        # TRC Header Data, ignore for now, can be used for finding timestamps, but I don't wanna
        if debug:
            print("This is a trc data header line")
        return "TRC Header Data"
    elif bool(re.search(r'\d+\)', data)):
        # TRC Log Data, translate to CAN data before processing
        if debug:
            print("This is a trc log line")

        can = "(0000000000.000000) can0 "
        data = data[33:]
        can += data[:3] + '#' + data[6:].replace(' ', '')
        data = can

        # print(can)
        ...
    else:
        return f"Unsupported data format; line: {data}"

    try:
        timestamp = re.findall(r'\(([^)]+)\)', data)[0]
        data: str = trim_can_input(data)
        sensor_id: str = get_sensor_id(data)
        sensor_id_int: int = int(sensor_id, 16)
        sensor_data: str = get_sensor_data(data)
        if debug:
            print(f"Data: {data}")
            print(f"Timestamp: {timestamp}")
            print(f"Sensor ID: {sensor_id}")
            print(f"Sensor ID (int): {sensor_id_int}")
            print(f"Sensor Data: {sensor_data}")

        # convert timestamp from unix time to human-readable time
        out = f'[{str(datetime.datetime.fromtimestamp(float(timestamp)))}] '

        # CMU Sensor are parsed differently here due to the range of values that they can have
        # that all have the same exact code
        if 0x301 <= sensor_id_int <= 0x3F3:
            if debug:
                print("This should be a CMU sensor")
            return parse_cmu_sensor(sensor_id_int, sensor_data, out)

        match sensor_id_int:
            # Heartbeat Sensor
            case 0x300:
                out += "BMU Heartbeat Sensor; "
                hb_id = hex_to_uint32(sensor_data[:8])
                hb_serial_number = hex_to_uint32(sensor_data[8:16])
                out += f"Device ID: {hb_id}; Serial Number: {hb_serial_number}"

                return out

            case 0x3F4:
                out += "Pack SoC; "
                pack_soc = hex_to_float(sensor_data[:8])
                pack_soc_percent = hex_to_float(sensor_data[8:16])
                out += f"Pack SoC: {pack_soc}aH; Pack SoC Percent: {pack_soc_percent}"

                return out

            case 0x3F5:
                out += "Pack Balance SoC; "
                pack_balance_soc = hex_to_float(sensor_data[:8])
                pack_balance_soc_percent = hex_to_float(sensor_data[8:16])
                out += f"Pack Balance SoC: {pack_balance_soc}aH; Pack Balance SoC Percent: {pack_balance_soc_percent}"

                return out

            case 0x3F6:
                # Note, data comes through this channel 10x as fast as other channels
                # Values are calculated based on preconfigured values, may result in errors with sample data?
                out += "Charger Control Info; "
                charging_cell_voltage_error = hex_to_int16(sensor_data[:4])
                charging_cell_temp_margin = hex_to_int16(sensor_data[4:8]) / 10 # should error on a zero value
                discharge_cell_voltage_error = hex_to_int16(sensor_data[8:12])
                total_pack_capacity = hex_to_uint16(sensor_data[12:16]) # preset value?
                out += f"Charging Cell Voltage Error: {charging_cell_voltage_error}mV; Charging Cell Temp Margin: {charging_cell_temp_margin}°C; Discharge Cell Voltage Error: {discharge_cell_voltage_error}mV; Total Pack Capacity: {total_pack_capacity}Ah"

                return out

            case 0x3F7:
                # print(sensor_data)
                out += "Precharge Status; "
                precharge_contactor_status = hex_to_uint8(sensor_data[:2])
                precharge_state = hex_to_uint8(sensor_data[2:4])
                match precharge_state:
                    case 0:
                        precharge_state = f"Error ({precharge_state})"
                    case 1:
                        precharge_state = f"Idle ({precharge_state})"
                    case 2:
                        precharge_state = f"Measure ({precharge_state})"
                    case 3:
                        precharge_state = f"Precharge ({precharge_state})"
                    case 4:
                        precharge_state = f"Run ({precharge_state})"
                    case 5:
                        precharge_state = f"Enable Pack ({precharge_state})"

                contactor_supply_voltage = hex_to_uint16(sensor_data[4:8]) # could be useless?
                # 8 : 12 garbage
                precharge_timer_status = hex_to_uint8(sensor_data[12:14]) # ignore if timeout is disabled
                match precharge_timer_status:
                    case 0:
                        precharge_timer_status = f"Disabled ({precharge_timer_status})"
                    case 1:
                        precharge_timer_status = f"Enabled ({precharge_timer_status})"
                precharge_timer_value = hex_to_uint8(sensor_data[14:16]) * 10
                out += f"Precharge Contactor Status: {precharge_contactor_status}; Precharge State: {precharge_state}; Contactor Supply Voltage: {contactor_supply_voltage}mV; Precharge Timer Status: {precharge_timer_status}; Precharge Timer Value: {precharge_timer_value}ms"

                return out

            case 0x3F8:
                # Note that this is a 10x faster channel
                out += "Min / Max Cell Voltage; "
                min_cell_voltage = hex_to_uint16(sensor_data[:4])
                max_cell_voltage = hex_to_uint16(sensor_data[4:8])
                cmu_with_min_voltage = hex_to_uint8(sensor_data[8:10])
                cell_with_min_voltage = hex_to_uint8(sensor_data[10:12])
                cmu_with_max_voltage = hex_to_uint8(sensor_data[12:14])
                cell_with_max_voltage = hex_to_uint8(sensor_data[14:16])
                out += f"Min Cell Voltage: {min_cell_voltage}mV; Max Cell Voltage: {max_cell_voltage}mV; CMU with Min Voltage: {cmu_with_min_voltage}; Cell with Min Voltage: {cell_with_min_voltage}; CMU with Max Voltage: {cmu_with_max_voltage}; Cell with Max Voltage: {cell_with_max_voltage}"

                return out

            case 0x3F9:
                out += "Min / Max Cell Temp; "
                min_cell_temp = hex_to_uint16(sensor_data[:4]) / 10
                max_cell_temp = hex_to_uint16(sensor_data[4:8]) / 10
                cmu_with_min_temp = hex_to_uint8(sensor_data[8:10])
                cell_with_min_temp = hex_to_uint8(sensor_data[10:12]) # unused
                cmu_with_max_temp = hex_to_uint8(sensor_data[12:14])
                cell_with_max_temp = hex_to_uint8(sensor_data[14:16]) # unused
                out += f"Min Cell Temp: {min_cell_temp}°C; Max Cell Temp: {max_cell_temp}°C; CMU with Min Temp: {cmu_with_min_temp}; CMU with Max Temp: {cmu_with_max_temp};"

                return out

            case 0x3FA:
                out += "Battery Pack Info; "
                pack_voltage = hex_to_uint32(sensor_data[:8])
                pack_current = hex_to_int32(sensor_data[8:16])
                out += f"Pack Voltage: {pack_voltage}mV; Pack Current: {pack_current}mA"

                return out

            case 0x3FB:
                out += "Battery Pack Status; "
                balance_voltage_threshold_rising = hex_to_uint16(sensor_data[:4])
                balance_voltage_threshold_falling = hex_to_uint16(sensor_data[4:8])
                pack_status = hex_to_uint8(sensor_data[8:10]) # unused potentially?
                cmu_count = hex_to_uint8(sensor_data[10:12])
                bmu_firmware_build_number = hex_to_uint16(sensor_data[12:16])
                out += f"Balance Voltage Threshold Rising: {balance_voltage_threshold_rising}mV; Balance Voltage Threshold Falling: {balance_voltage_threshold_falling}mV; CMU Count: {cmu_count}; BMU Firmware Build Number: {bmu_firmware_build_number}"

                return out

            case 0x3FC:
                out += "Battery Pack Fan Status; "
                fan_0_speed = hex_to_uint16(sensor_data[:4])
                fan_1_speed = hex_to_uint16(sensor_data[4:8])
                current_consumption_fans_and_contactors = hex_to_uint16(sensor_data[8:12])
                current_consumption_cmus = hex_to_uint16(sensor_data[12:16])
                out += f"Fan 0 Speed: {fan_0_speed}rpm; Fan 1 Speed: {fan_1_speed}rpm; Current Consumption Fans and Contactors: {current_consumption_fans_and_contactors}mA; Current Consumption CMUs: {current_consumption_cmus}mA"

                return out

            case 0x3FD:
                out += "Extended Battery Pack Info; "
                pack_status = hex_to_uint32(sensor_data[:8])
                bmu_hardware_version = hex_to_uint8(sensor_data[8:10])
                bmu_model_id = hex_to_uint8(sensor_data[10:12])
                # 12 : 16 garbage
                out += f"Pack Status: {pack_status}; BMU Hardware Version: {bmu_hardware_version}; BMU Model ID: {bmu_model_id}"

                return out

            case _:
                return f"Sensor ID {sensor_id} not recognized; Data: {sensor_data[:-1]}"

    except Exception as e:
        print("Something happen:(")
        return f"Error: {e}"

def trim_can_input(data: str) -> str:
    """ Trim the CAN data input to only the data portion """
    data = data.split(' ')
    return data[2]


def get_sensor_id(data: str) -> str:
    """ Get the sensor id from the CAN data cleaned with trim_can_input """
    sensor_id = data[:3]

    return hex(int(sensor_id, 16))

def get_sensor_data(data: str) -> str:
    """ Get the sensor data from the CAN data cleaned with trim_can_input """
    data = data.split('#')
    return data[1]




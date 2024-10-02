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

def hex_to_bits(hex_str):
    # convert a string of hex values to its equivalent binary string then fill in the missing 0s
    return bin(int(hex_inverter(hex_str), 16))[2:].zfill(len(hex_str) * 4)

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
        cmu_pcb_temp = round(hex_to_int16(sensor_data[8:12]) / 10, 3)
        cmu_cell_temp = round(hex_to_int16(sensor_data[12:16]) / 10, 3)
        out += f"Serial Number: {cmu_serial_number}; PCB Temp: {cmu_pcb_temp}°C; Cell Temp: {cmu_cell_temp}°C"

    elif part == 1:  # Cell voltages 0-3
        c0_voltage = round(hex_to_int16(sensor_data[:4]) / 1000, 3)
        c1_voltage = round(hex_to_int16(sensor_data[4:8]) / 1000, 3)
        c2_voltage = round(hex_to_int16(sensor_data[8:12]) / 1000, 3)
        c3_voltage = round(hex_to_int16(sensor_data[12:16]) / 1000, 3)
        out += f"Cell 0 Voltage: {c0_voltage}V; Cell 1 Voltage: {c1_voltage}V; Cell 2 Voltage: {c2_voltage}V; Cell 3 Voltage: {c3_voltage}V"

    elif part == 2:  # Cell voltages 4-7
        c4_voltage = round(hex_to_int16(sensor_data[:4]) / 1000, 3)
        c5_voltage = round(hex_to_int16(sensor_data[4:8]) / 1000, 3)
        c6_voltage = round(hex_to_int16(sensor_data[8:12]) / 1000, 3)
        c7_voltage = round(hex_to_int16(sensor_data[12:16]) / 1000, 3)
        out += f"Cell 4 Voltage: {c4_voltage}V; Cell 5 Voltage: {c5_voltage}V; Cell 6 Voltage: {c6_voltage}V; Cell 7 Voltage: {c7_voltage}V"
    else:
        print("What happen:(?")
        return f"CMU Sensor {sensor_index} part {part} not recognized; Data: {sensor_data[:-1]}"

    return out + '\n'

def parse_can_line(data: str, debug: bool) -> str:
    trc_timestamp: datetime = datetime.datetime.fromtimestamp(float('0000000000.000000'))
    if data[0] == '(':
        # Normal CAN data, continue as normal
        if debug:
            print("This is a CAN log line")
    elif data[0] == ';':
        # TRC Header Data, ignore for now, can be used for finding timestamps, but I don't wanna
        if debug:
            print("This is a trc data header line")
        if data.__contains__('TIMESTAMP'):
            trc_timestamp += datetime.datetime.fromtimestamp(float(data.split('TIMESTAMP')[1]))
        return "TRC Header Data" + '\n'
    elif bool(re.search(r'\d+\)', data)):
        # TRC Log Data, translate to CAN data before processing
        if debug:
            print("This is a trc log line")

        print(f'Original Timestamp: {trc_timestamp}')
        offset_timestamp: datetime = datetime.datetime.fromtimestamp(float(re.findall(r'\d*\.?\d', data)[0]))
        trc_timestamp.__add__(offset_timestamp)
        print(f'Offset Timestamp: {offset_timestamp}')
        can = "(0000000000.000000) can0 "
        data = data[33:]
        can += data[:3] + '#' + data[6:].replace(' ', '')
        data = can

        # print(can)
    elif data.startswith('Timestamp'):
        if debug:
            print("This is a PCAN log line")
        can = f"({data.split('Timestamp')[1].split(' ')[1]}) can0 "
        sensor = data.split('ID:')[1][:9].replace(' ', '')
        data = data.split('DL:  8')[1][:102-75].replace(' ', '')
        can += sensor + '#' + data
        # print(can)
        data = can
    else:
        return f"Unsupported data format; line: {data}" + '\n'

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

                return out + '\n'

            case 0x3F4:
                out += "Pack SoC; "
                pack_soc = round(hex_to_float(sensor_data[:8]), 3)
                pack_soc_percent = round(hex_to_float(sensor_data[8:16]) * 100, 3)
                out += f"Pack SoC: {pack_soc}Ah; Pack SoC Percent: {pack_soc_percent}%"

                return out + '\n'

            case 0x3F5:
                out += "Pack Balance SoC; "
                pack_balance_soc = round(hex_to_float(sensor_data[:8]), 3)
                pack_balance_soc_percent = round(hex_to_float(sensor_data[8:16]) * 100, 3)
                out += f"Pack Balance SoC: {pack_balance_soc}Ah; Pack Balance SoC Percent: {pack_balance_soc_percent}%"

                return out + '\n'

            case 0x3F6:
                # Note, data comes through this channel 10x as fast as other channels
                # Values are calculated based on preconfigured values, may result in errors with sample data?
                out += "Charger Control Info; "
                charging_cell_voltage_error = round(hex_to_int16(sensor_data[:4]) * 1000, 3)
                charging_cell_temp_margin = hex_to_int16(sensor_data[4:8]) / 10 # should error on a zero value
                discharge_cell_voltage_error = hex_to_int16(sensor_data[8:12])
                total_pack_capacity = hex_to_uint16(sensor_data[12:16]) # preset value?
                out += f"Charging Cell Voltage Error: {charging_cell_voltage_error}mV; Charging Cell Temp Margin: {charging_cell_temp_margin}°C; Discharge Cell Voltage Error: {discharge_cell_voltage_error}mV; Total Pack Capacity: {total_pack_capacity}Ah"

                # Configuration data, ignore
                return ""

            case 0x3F7:
                # print(sensor_data)
                out += "Precharge Status; "
                precharge_contactor_status = hex_to_bits(sensor_data[:2])[::-1]
                if debug:
                    print(f'Bits for data_u8[0]: {precharge_contactor_status}')
                precharge_contactor_status = f'Contactor 1 Driver Error [{bool(int(precharge_contactor_status[0]))}] ' + \
                                            f'Contactor 2 Driver Error [{bool(int(precharge_contactor_status[1]))}] ' + \
                                            f'Contactor 3 Driver Error [{bool(int(precharge_contactor_status[5]))}] ' + \
                                            f'Contactor 1 Status [{bool(int(precharge_contactor_status[2]))}] ' + \
                                            f'Contactor 2 Status [{bool(int(precharge_contactor_status[3]))}] ' + \
                                            f'Contactor 3 Status [{bool(int(precharge_contactor_status[6]))}] ' + \
                                            f'12V Contactor Supply Voltage [{bool(int(precharge_contactor_status[4]))}] '
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

                contactor_supply_voltage = round(hex_to_uint16(sensor_data[4:8]) * 1000, 3) # could be useless?
                # 8 : 12 garbage
                precharge_timer_status = hex_to_bits(sensor_data[12:14]) # ignore if timeout is disabled
                precharge_timer_value = round(hex_to_uint8(sensor_data[14:16]) * 10 / 1000, 3)
                out += f"Precharge Contactor Status: {precharge_contactor_status}; Precharge State: {precharge_state}; Contactor Supply Voltage: {contactor_supply_voltage}V; Precharge Timer Status: {precharge_timer_status}; Precharge Timer Value: {precharge_timer_value}s"

                return out + '\n'

            case 0x3F8:
                # Note that this is a 10x faster channel
                out += "Min / Max Cell Voltage; "
                min_cell_voltage = round(hex_to_uint16(sensor_data[:4]) / 1000, 3)
                max_cell_voltage = round(hex_to_uint16(sensor_data[4:8]) / 1000, 3)
                cmu_with_min_voltage = hex_to_uint8(sensor_data[8:10])
                cell_with_min_voltage = hex_to_uint8(sensor_data[10:12])
                cmu_with_max_voltage = hex_to_uint8(sensor_data[12:14])
                cell_with_max_voltage = hex_to_uint8(sensor_data[14:16])
                out += f"Min Cell Voltage: {min_cell_voltage}V; Max Cell Voltage: {max_cell_voltage}V; CMU with Min Voltage: {cmu_with_min_voltage}; Cell with Min Voltage: {cell_with_min_voltage}; CMU with Max Voltage: {cmu_with_max_voltage}; Cell with Max Voltage: {cell_with_max_voltage}"

                return out + '\n'

            case 0x3F9:
                out += "Min / Max Cell Temp; "
                min_cell_temp = hex_to_uint16(sensor_data[:4]) / 10
                max_cell_temp = hex_to_uint16(sensor_data[4:8]) / 10
                cmu_with_min_temp = hex_to_uint8(sensor_data[8:10])
                cell_with_min_temp = hex_to_uint8(sensor_data[10:12]) # unused
                cmu_with_max_temp = hex_to_uint8(sensor_data[12:14])
                cell_with_max_temp = hex_to_uint8(sensor_data[14:16]) # unused
                out += f"Min Cell Temp: {min_cell_temp}°C; Max Cell Temp: {max_cell_temp}°C; CMU with Min Temp: {cmu_with_min_temp}; CMU with Max Temp: {cmu_with_max_temp};"

                return out + '\n'

            case 0x3FA:
                out += "Battery Pack Info; "
                pack_voltage = round(hex_to_uint32(sensor_data[:8]) / 1000, 3)
                pack_current = round(hex_to_int32(sensor_data[8:16]) / 1000, 3)
                out += f"Pack Voltage: {pack_voltage}V; Pack Current: {pack_current}A"

                return out + '\n'

            case 0x3FB:
                out += "Battery Pack Status; "
                balance_voltage_threshold_rising = hex_to_uint16(sensor_data[:4])
                balance_voltage_threshold_falling = hex_to_uint16(sensor_data[4:8])
                pack_status = hex_to_uint8(sensor_data[8:10]) # deprecated by 0x3FD[0]
                cmu_count = hex_to_uint8(sensor_data[10:12])
                bmu_firmware_build_number = hex_to_uint16(sensor_data[12:16])
                out += f"Balance Voltage Threshold Rising: {balance_voltage_threshold_rising}mV; Balance Voltage Threshold Falling: {balance_voltage_threshold_falling}mV; CMU Count: {cmu_count}; BMU Firmware Build Number: {bmu_firmware_build_number}"

                return out + '\n'

            case 0x3FC:
                out += "Battery Pack Fan Status; "
                fan_0_speed = hex_to_uint16(sensor_data[:4])
                fan_1_speed = hex_to_uint16(sensor_data[4:8])
                current_consumption_fans_and_contactors = round(hex_to_uint16(sensor_data[8:12]) / 1000, 3)
                current_consumption_cmus = round(hex_to_uint16(sensor_data[12:16]) / 1000, 3)
                out += f"Fan 0 Speed: {fan_0_speed}rpm; Fan 1 Speed: {fan_1_speed}rpm; Current Consumption Fans and Contactors: {current_consumption_fans_and_contactors}A; Current Consumption CMUs: {current_consumption_cmus}A"

                return out + '\n'

            case 0x3FD:
                out += "Extended Battery Pack Info; "
                pack_status = hex_to_bits(sensor_data[:8])
                if debug:
                    print(f'Bits for data_u32[0]: {pack_status}')
                pack_status = f'Cell Over Voltage [{bool(int(pack_status[0]))}] ' + \
                                f'Cell Under Voltage [{bool(int(pack_status[1]))}] ' + \
                                f'Cell Over Temp [{bool(int(pack_status[2]))}] ' + \
                                f'Measurement Untrusted (channel mismatch) [{bool(int(pack_status[3]))}] ' + \
                                f'CMU Communications Timeout (lost CMU) [{bool(int(pack_status[4]))}] ' + \
                                f'Vehicle Communications Timeout (lost EVDC) [{bool(int(pack_status[5]))}] ' + \
                                f'BMU Setup Mode [{bool(int(pack_status[6]))}] ' + \
                                f'CMU CAN Bus Power Status [{bool(int(pack_status[7]))}] ' + \
                                f'Pack Isolation Test Failure [{bool(int(pack_status[8]))}] ' + \
                                f'SoC Measurement Invalid [{bool(int(pack_status[9]))}] ' + \
                                f'CAN 12V Supply Low [{bool(int(pack_status[10]))}] ' + \
                                f'Contactor Stuck or Disenganged [{bool(int(pack_status[11]))}] ' + \
                                f'CMU Detected Extra Cell Present [{bool(int(pack_status[12]))}] '
                bmu_hardware_version = hex_to_uint8(sensor_data[8:10])
                bmu_model_id = hex_to_uint8(sensor_data[10:12])
                # 12 : 16 garbage
                out += f"Pack Status: {pack_status}; BMU Hardware Version: {bmu_hardware_version}; BMU Model ID: {bmu_model_id}"

                return out + '\n'

            case 0x600:
                out += "MPPT 1 Input; "
                mppt_input_voltage = round(hex_to_float(sensor_data[:8]), 3)
                mppt_input_current = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"MPPT 1 Input Voltage: {mppt_input_voltage}V; MPPT 1 Input Current: {mppt_input_current}A"

                return out + '\n'

            case 0x601:
                out += "MPPT 1 Output; "
                mppt_output_voltage = round(hex_to_float(sensor_data[:8]), 3)
                mppt_output_current = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"MPPT 1 Output Voltage: {mppt_output_voltage}V; MPPT 1 Output Current: {mppt_output_current}A"

                return out + '\n'

            case 0x602:
                out += "MPPT 1  Temperature; "
                mosfet_temp = round(hex_to_float(sensor_data[:8]), 3)
                controller_temp = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"MOSFET Temp: {mosfet_temp}°C; Controller Temp: {controller_temp}°C"

                return out + '\n'

            case 0x603:
                out += "MPPT 1 Auxiliary Power Supply; "
                v12 = round(hex_to_float(sensor_data[:8]), 3)
                v3 = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"12V: {v12}V; 3V: {v3}V"

                return out + '\n'

            case 0x604:
                out += "MPPT 1 Limits; "
                max_output_voltage = round(hex_to_float(sensor_data[:8]), 3)
                max_input_current = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"Max Output Voltage: {max_output_voltage}V; Max Input Current: {max_input_current}A"

                return out + '\n'

            case 0x605:
                out += "MPPT 1 Status; "
                can_rx_error_count = hex_to_uint8(sensor_data[:2])
                can_tx_error_count = hex_to_uint8(sensor_data[2:4])
                can_tx_overflow_count = hex_to_uint8(sensor_data[4:6])
                error_flag = hex_to_uint8(sensor_data[6:8])
                limit_flag = hex_to_uint8(sensor_data[8:10])
                mode = hex_to_uint8(sensor_data[10:12])
                match mode:
                    case 0:
                        mode = "Standby (0)"
                    case 1:
                        mode = "On (1)"
                    case _:
                        mode = "Unknown"
                # 12 : 14 garbage
                test_counter = hex_to_uint8(sensor_data[14:16]) # unsure of what this is for?
                out += f"CAN RX Error Count: {can_rx_error_count}; CAN TX Error Count: {can_tx_error_count}; CAN TX Overflow Count: {can_tx_overflow_count}; Error Flag: {error_flag}; Limit Flag: {limit_flag}; Mode: {mode}; Test Counter: {test_counter}"

                return out + '\n'

            case 0x606:
                out += "MPPT 1 Power Connector; "
                output_voltage = round(hex_to_float(sensor_data[:8]), 3)
                connector_temp = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"Output Voltage: {output_voltage}V; Connector Temp: {connector_temp}°C"

                return out + '\n'

            case 0x608:
                out += "MPPT 1 Mode (Send)"
                mode = hex_to_uint8(sensor_data[:2])
                # 2 : 16 garbage
                out += f"Mode (send): {mode}"

                return out + '\n'

            case 0x60A:
                out += "MPPT 1 Maximum Output Voltage (send); "
                max_output_voltage = hex_to_float(sensor_data[:8])
                # 8 : 16 garbage
                out += f"Max Output Voltage (send): {max_output_voltage}V"

                return out + '\n'

            case 0x60B:
                out += "MPPT 1 Maximum Input Current (send); "
                max_input_current = hex_to_float(sensor_data[:8])
                # 8 : 16 garbage
                out += f"Max Input Current (send): {max_input_current}A"

                return out + '\n'

            case 0x610:
                out += "MPPT 2 Input; "
                mppt_input_voltage = round(hex_to_float(sensor_data[:8]), 3)
                mppt_input_current = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"MPPT 2 Input Voltage: {mppt_input_voltage}V; MPPT 2 Input Current: {mppt_input_current}A"

                return out + '\n'

            case 0x611:
                out += "MPPT 2 Output; "
                mppt_output_voltage = round(hex_to_float(sensor_data[:8]), 3)
                mppt_output_current = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"MPPT 2 Output Voltage: {mppt_output_voltage}V; MPPT 2 Output Current: {mppt_output_current}A"

                return out + '\n'

            case 0x612:
                out += "MPPT 2  Temperature; "
                mosfet_temp = round(hex_to_float(sensor_data[:8]), 3)
                controller_temp = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"MOSFET Temp: {mosfet_temp}°C; Controller Temp: {controller_temp}°C"

                return out + '\n'

            case 0x613:
                out += "MPPT 2 Auxiliary Power Supply; "
                v12 = round(hex_to_float(sensor_data[:8]), 3)
                v3 = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"12V: {v12}V; 3V: {v3}V"

                return out + '\n'

            case 0x614:
                out += "MPPT 2 Limits; "
                max_output_voltage = round(hex_to_float(sensor_data[:8]), 3)
                max_input_current = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"Max Output Voltage: {max_output_voltage}V; Max Input Current: {max_input_current}A"

                return out + '\n'

            case 0x615:
                out += "MPPT 2 Status; "
                can_rx_error_count = hex_to_uint8(sensor_data[:2])
                can_tx_error_count = hex_to_uint8(sensor_data[2:4])
                can_tx_overflow_count = hex_to_uint8(sensor_data[4:6])
                error_flag = hex_to_uint8(sensor_data[6:8])
                limit_flag = hex_to_uint8(sensor_data[8:10])
                mode = hex_to_uint8(sensor_data[10:12])
                match mode:
                    case 0:
                        mode = "Standby (0)"
                    case 1:
                        mode = "On (1)"
                    case _:
                        mode = "Unknown"
                # 12 : 14 garbage
                test_counter = hex_to_uint8(sensor_data[14:16])  # unsure of what this is for?
                out += f"CAN RX Error Count: {can_rx_error_count}; CAN TX Error Count: {can_tx_error_count}; CAN TX Overflow Count: {can_tx_overflow_count}; Error Flag: {error_flag}; Limit Flag: {limit_flag}; Mode: {mode}; Test Counter: {test_counter}"

                return out + '\n'

            case 0x616:
                out += "MPPT 2 Power Connector; "
                output_voltage = round(hex_to_float(sensor_data[:8]), 3)
                connector_temp = round(hex_to_float(sensor_data[8:16]), 3)
                out += f"Output Voltage: {output_voltage}V; Connector Temp: {connector_temp}°C"

                return out + '\n'

            case 0x618:
                out += "MPPT 2 Mode (Send)"
                mode = hex_to_uint8(sensor_data[:2])
                # 2 : 16 garbage
                out += f"Mode (send): {mode}"

                return out + '\n'

            case 0x61A:
                out += "MPPT 2 Maximum Output Voltage (send); "
                max_output_voltage = hex_to_float(sensor_data[:8])
                # 8 : 16 garbage
                out += f"Max Output Voltage (send): {max_output_voltage}V"

                return out + '\n'

            case 0x61B:
                out += "MPPT 2 Maximum Input Current (send); "
                max_input_current = hex_to_float(sensor_data[:8])
                # 8 : 16 garbage
                out += f"Max Input Current (send): {max_input_current}A"

                return out + '\n'
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




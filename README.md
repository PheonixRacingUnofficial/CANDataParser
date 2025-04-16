# FPU CAN Parser

## Overview

**fpu\_can\_parser** is a Python module that parses and interprets CAN (Controller Area Network) data logs. It supports multiple log formats (Standard CAN, TRC, and PCAN) and uses customizable sensor definitions to convert raw hexadecimal data into structured sensor values.

This tool is especially useful for electric vehicle telemetry and other embedded systems that output CAN logs with unique sensor configurations.

---

## Installation

Install directly from GitHub using `pip`:

```bash
pip install git+https://github.com/PheonixRacingUnofficial/CANDataParser
```

---

## Quick Start

### 1. Create a Sensor Definitions File

This file defines your sensor mappings and should look like this:

```
0x300,bmuhbs,%ui32%ui32,%hbid%hbsn
```

Each line format:

```
<sensor_id>,<sensor_name_code>,<sensor_data_format>,<sensor_data_description_code>
```

Refer to [`Sensor.md`](fpu_can_parser/parser/documentation/Sensor.md) and [`SensorAlias.md`](fpu_can_parser/parser/documentation/SensorAlias.md) for more information on format and naming.

---

### 2. Create a Parser and Use It

```python
from fpu_can_parser.parser import Parser

# Create a parser with a path to your sensor definition file
parser = Parser("path/to/sensor_file.txt", debug=True)

# Parse CAN log lines one by one
parsed = parser.parse_can_line("(1687282000.123456) can0 300#05500000AB0D0000")

print(parsed)
```

**Example Output:**

```python
('2023-06-20 12:33:20.123456', '0x300', {'hbid': '550', 'hbsn': '3499'})
```

---

## Architecture

- [`Parser`](Parser.md): Handles CAN line format parsing, timestamp normalization, and sensor value decoding.
- [`Sensor`](Sensor.md): Defines individual sensors, their format codes, and how to parse data for each.
- [`SensorManager`](SensorManager.md): Loads and manages all defined sensors and routes CAN data appropriately.
- [`SensorAlias`](SensorAlias.md): Provides definitions for abbreviations used in sensor names and data descriptions.

---

## Output Format

Each call to `parser.parse_can_line()` returns:

```python
(datetime_string, sensor_id_string, sensor_data_dict)
```

For example:

```python
('2023-06-20 12:33:20.123456', '0x300', {'hbid': '550', 'hbsn': '3499'})
```

---

## Unit Testing

This module includes a comprehensive test suite built using Python's `unittest` framework.

### Files:

- `test_hex_helper.py`: Tests all `hex_helper` conversion functions (e.g., `hex_to_int8`, `hex_to_float`, `hex_to_bits`, etc.).
- `test_parser.py`: Tests high-level integration of parsing from CAN, TRC, and PCAN lines, and validates behavior from `Sensor`, `SensorManager`, and `Parser` components.

### Running Tests:

Run all unit tests using:

```bash
python -m unittest discover
```

Or run individual files:

```bash
python -m unittest test/test_parser.py
python -m unittest test/test_hex_helper.py
```

These tests verify correctness, error handling, and output formatting, and help ensure robust performance across the module.

---

## License and Contributing

This project is open source under the [MIT License](https://opensource.org/licenses/MIT).

Contributions are welcome! Feel free to fork, submit issues, or create pull requests to extend functionality or adapt to your custom sensor configurations.


# Parser

## Overview
`Parser` is a Python module designed to read and interpret CAN (Controller Area Network) log data. It supports multiple CAN data formats—including standard CAN, TRC log, and PCAN log formats—and uses a `SensorManager` to translate the raw data into readable and structured sensor output.

## Features
- Parses standard CAN, TRC, and PCAN log formats.
- Extracts timestamps, sensor IDs, and raw data.
- Converts sensor data using predefined format definitions via `SensorManager`.
- Outputs structured sensor data in dictionary format.
- Logs debug information using the `Logger` class.

## Supported Formats

### Standard CAN Format
```
(timestamp) can0 ID#data
```

### TRC Log Format
```
<index> <timestamp> <flags> <channel> <ID> <length> <data bytes>...
```

### PCAN Log Format
```
Timestamp: <time> Type: <type> ID: <id> DL:  8 Data: <bytes>
```

All formats are normalized to a standard CAN string before parsing.

## Usage

You can use the `Parser` class by importing it and initializing with a sensor definition file:

```python
from fpu_can_parser.parser.Parser import Parser

parser = Parser("path/to/sensor_file.txt", debug=True)
parsed = parser.parse_can_line("(1687282000.123456) can0 300#05500000AB0D0000")

print(parsed)
```

Example output:
```python
('2023-06-20 12:33:20.123456', '0x300', {'hbid': '550', 'hbsn': '3499'})
```

## Functionality

### `Parser`

#### `__init__(sensor_file: str, debug: bool = False, log: bool = False)`
- Initializes the `Parser` object.
- Loads the sensor definitions and sets up the logger.

**Parameters:**
- `sensor_file`: Path to the sensor definition file.
- `debug`: If `True`, enables debug logs.
- `log`: If `True`, enables file logging.

#### `parse_can_line(data: str) -> Tuple[str, str, Dict[str, str]] | None`
- Parses a single line of CAN data and returns a tuple containing the timestamp, sensor ID, and parsed sensor data.
- If the line is a TRC header, it updates the internal timestamp and returns `None`.

**Returns:**
- `Tuple[str, str, Dict[str, str]]` or `None`

**Example:**
```python
('2023-06-20 12:33:20.123456', '0x300', {'hbid': '550', 'hbsn': '3499'})
```

---

### `translate_can_format(data: str) -> str`
- Converts raw TRC or PCAN formatted lines into standard CAN format.
- Returns a normalized CAN string.

**Raises:**
- `ValueError`: If the input format is unsupported.

## Error Handling
- **ValueError**: Raised when an unsupported data format is encountered.
- Lines that begin with `;` and contain the word `TIMESTAMP` will update the internal TRC timestamp.

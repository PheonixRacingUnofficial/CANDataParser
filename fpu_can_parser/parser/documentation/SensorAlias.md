# Sensor Descriptor Alias

## Sensor Names

| Abbreviation  | Full Meaning                 |
|---------------|------------------------------|
| bmuhbs        | BMU Heartbeat Sensor         |
| packsoc       | Pack State of Charge Sensor  |
| packbalsoc    | Pack Balance State of Charge |
| chargerctl    | Charger Control Info         |
| prechargestat | Precharge Status             |
| minmaxv       | Min / Max Cell Voltage       |
| minmaxt       | Min / Max Cell Temperature   |
| packinfo      | Battery Pack Info            |
| packstatus    | Battery Pack Status          |
| fanstatus     | Battery Pack Fan Status      |
| packextinfo   | Extended Battery Pack Info   |
| mppt#i        | MPPT# Input                  |
| mppt#o        | MPPT# Output                 |
| mppt#t        | MPPT# Temperature            |
| mppt#aps      | MPPT# Auxiliary Power Supply |
| mppt#l        | MPPT# Limits                 |
| mppt#s        | MPPT# Status                 |
| mppt#pc       | MPPT# Power Connector        |
| cmu#s         | CMU# Status                  |
| cmu#v1        | CMU# Cell Voltages Set 1     |
| cmu#v2        | CMU# Cell Voltages Set 2     |


## Sensor Data

| Abbreviation | Description                                 |
|--------------|---------------------------------------------|
| hbid         | Device ID                                   |
| hbsn         | Serial Number                               |
| soc          | State of Charge (Ah)                        |
| socp         | State of Charge Percentage (%)              |
| balsoc       | Balance SoC (Ah)                            |
| balsocp      | Balance SoC Percentage                      |
| cverr        | Charging Cell Voltage Error (mV)            |
| ctmarg       | Charging Cell Temp Margin (°C)              |
| dverr        | Discharge Cell Voltage Error (mV)           |
| tpcap        | Total Pack Capacity (Ah)                    |
| pcs          | Precharge Contactor Status                  |
| pstate       | Precharge State                             |
| csv          | Contactor Supply Voltage (V)                |
| pts          | Precharge Timer Status                      |
| ptv          | Precharge Timer Value (s)                   |
| minv         | Minimum Cell Voltage                        |
| maxv         | Maximum Cell Voltage                        |
| cmuminv      | CMU with Minimum Voltage (V)                |
| cellminv     | Cell with Minimum Voltage (V)               |
| cmumaxv      | CMU with Maximum Voltage (V)                |
| cellmaxv     | Cell with Maximum Voltage (V)               |
| mint         | Minimum Cell Temperature (°C)               |
| maxt         | Maximum Cell Temperature (°C)               |
| cmumint      | CMU with Minimum Temperature (°C)           |
| cellmint     | Cell with Minimum Temperature (°C)          |
| cmumaxt      | CMU with Maximum Temperature (°C)           |
| cellmaxt     | Cell with Maximum Temperature (°C)          |
| pvoltage     | Pack Voltage (V)                            |
| pcurrent     | Pack Current (A)                            |
| bvthr        | Balance Voltage Threshold Rising (mV)       |
| bvthf        | Balance Voltage Threshold Falling (mV)      |
| ps           | Pack Status (deprecated)                    |
| cmucnt       | CMU Count                                   |
| bbuild       | BMU Firmware Build Number                   |
| fan0         | Fan 0 Speed (rpm)                           |
| fan1         | Fan 1 Speed (rpm)                           |
| curfancon    | Current Consumption Fans and Contactors (A) |
| curcmu       | Current Consumption CMUs (A)                |
| psbits       | Pack Status Bitfield (extended flags)       |
| bhwver       | BMU Hardware Version                        |
| bmodel       | BMU Model ID                                |


### MPPT Data

| Abbreviation     | Description                    |
|------------------|--------------------------------|
| mppt#iv          | MPPT# Input Voltage (V)        |
| mppt#ic          | MPPT# Input Current (A)        |
| mppt#ov          | MPPT# Output Voltage (V)       |
| mppt#oc          | MPPT# Output Current (A)       |
| mppt#mt          | MPPT# Mosfet Temperature (°C)  |
| mppt#ct          | MPPT# Control Temperature (°C) |
| mppt#_12v        | MPPT# 12V Supply Voltage (V)   |
| mppt#_3v         | MPPT# 3V Supply Voltage (V)    |
| mppt#mov         | MPPT# Max Output Voltage (V)   |
| mppt#mic         | MPPT# Max Input Current (A)    |
| mppt#canrxerrcnt | MPPT# CAN RX Error Count       |
| mppt#cantxerrcnt | MPPT# CAN TX Error Count       |
| mppt#cantxofcnt  | MPPT# CAN TX Overflow Count    |
| mppt#errflg      | MPPT# Error Flag               |
| mppt#limflg      | MPPT# Limit Flag               |
| mppt#mode        | MPPT# Mode                     |
| mppt#tstcnt      | MPPT# Test Count               |
| mppt#ovcon       | MPPT# Output Voltage Connector |
| mppt#ct          | MPPT# Connector Temp           |
 
### CMU Data
| Abbreviation | Description              |
|--------------|--------------------------|
| cmu#sn       | CMU Serial Number        |
| cmu#pcbt     | CMU PCB Temperature (°C) |
| cmu#ct       | CMU Cell Temperature (V) |
| cmu#v0       | CMU Cell Voltage 0 (V)   |
| cmu#v1       | CMU Cell Voltage 1 (V)   |
| cmu#v2       | CMU Cell Voltage 2 (V)   |
| cmu#v3       | CMU Cell Voltage 3 (V)   |
| cmu#v4       | CMU Cell Voltage 4 (V)   |
| cmu#v5       | CMU Cell Voltage 5 (V)   |
| cmu#v6       | CMU Cell Voltage 6 (V)   |
| cmu#v7       | CMU Cell Voltage 7 (V)   |


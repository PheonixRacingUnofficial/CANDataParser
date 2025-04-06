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

| Abbreviation | Description                                                |
|--------------|------------------------------------------------------------|
| hbid         | Device ID                                                  |
| hbsn         | Serial Number                                              |
| soc          | State of Charge (Ah) round 3                               |
| socp         | State of Charge Percentage (%) * 100 round 3               |
| balsoc       | Balance SoC (Ah) round 3                                   |
| balsocp      | Balance SoC Percentage * 100 round 3                       |
| cverr        | Charging Cell Voltage Error (mV) * 1000 round 3            |
| ctmarg       | Charging Cell Temp Margin (°C) / 10                        |
| dverr        | Discharge Cell Voltage Error (mV)                          |
| tpcap        | Total Pack Capacity (Ah)                                   |
| pcs          | Precharge Contactor Status                                 |
| pstate       | Precharge State                                            |
| csv          | Contactor Supply Voltage (V) * 1000 round 3                |
| pts          | Precharge Timer Status                                     |
| ptv          | Precharge Timer Value (s) * 10 / 1000 round 3              |
| minv         | Minimum Cell Voltage (V) / 1000 round 3                    |
| maxv         | Maximum Cell Voltage (V) / 1000 round 3                    |
| cmuminv      | CMU with Minimum Voltage (V)                               |
| cellminv     | Cell with Minimum Voltage (V)                              |
| cmumaxv      | CMU with Maximum Voltage (V)                               |
| cellmaxv     | Cell with Maximum Voltage (V)                              |
| mint         | Minimum Cell Temperature (°C) / 10                         |
| maxt         | Maximum Cell Temperature (°C) / 10                         |
| cmumint      | CMU with Minimum Temperature (°C)                          |
| cellmint     | Cell with Minimum Temperature (°C)                         |
| cmumaxt      | CMU with Maximum Temperature (°C)                          |
| cellmaxt     | Cell with Maximum Temperature (°C)                         |
| pvoltage     | Pack Voltage (V) / 1000 round 3                            |
| pcurrent     | Pack Current (A) / 1000 round 3                            |
| bvthr        | Balance Voltage Threshold Rising (mV)                      |
| bvthf        | Balance Voltage Threshold Falling (mV)                     |
| ps           | Pack Status (deprecated)                                   |
| cmucnt       | CMU Count                                                  |
| bbuild       | BMU Firmware Build Number                                  |
| fan0         | Fan 0 Speed (rpm)                                          |
| fan1         | Fan 1 Speed (rpm)                                          |
| curfancon    | Current Consumption Fans and Contactors (A) / 1000 round 3 |
| curcmu       | Current Consumption CMUs (A) / 1000 round 3                |
| psbits       | Pack Status Bitfield (extended flags)                      |
| bhwver       | BMU Hardware Version                                       |
| bmodel       | BMU Model ID                                               |


### MPPT Data

| Abbreviation     | Description                                |
|------------------|--------------------------------------------|
| mppt#iv          | MPPT# Input Voltage (V) round 3            |
| mppt#ic          | MPPT# Input Current (A) round 3            |
| mppt#ov          | MPPT# Output Voltage (V) round 3           |
| mppt#oc          | MPPT# Output Current (A) round 3           |
| mppt#mt          | MPPT# Mosfet Temperature (°C) round 3      |
| mppt#ct          | MPPT# Control Temperature (°C) round 3     |
| mppt#_12v        | MPPT# 12V Supply Voltage (V) round 3       |
| mppt#_3v         | MPPT# 3V Supply Voltage (V) round 3        |
| mppt#mov         | MPPT# Max Output Voltage (V) round 3       |
| mppt#mic         | MPPT# Max Input Current (A) round 3        |
| mppt#canrxerrcnt | MPPT# CAN RX Error Count                   |
| mppt#cantxerrcnt | MPPT# CAN TX Error Count                   |
| mppt#cantxofcnt  | MPPT# CAN TX Overflow Count                |
| mppt#errflg      | MPPT# Error Flag                           |
| mppt#limflg      | MPPT# Limit Flag                           |
| mppt#mode        | MPPT# Mode                                 |
| mppt#tstcnt      | MPPT# Test Count                           |
| mppt#ovcon       | MPPT# Output Voltage Connector (V) round 3 |
| mppt#ct          | MPPT# Connector Temp (°C) round 3          |
 
### CMU Data
| Abbreviation | Description                            |
|--------------|----------------------------------------|
| cmu#sn       | CMU Serial Number                      |
| cmu#pcbt     | CMU PCB Temperature (°C) / 10 round 3  |
| cmu#ct       | CMU Cell Temperature (°C) / 10 round 3 |
| cmu#v0       | CMU Cell Voltage 0 (V) / 1000 round 3  |
| cmu#v1       | CMU Cell Voltage 1 (V) / 1000 round 3  |
| cmu#v2       | CMU Cell Voltage 2 (V) / 1000 round 3  |
| cmu#v3       | CMU Cell Voltage 3 (V) / 1000 round 3  |
| cmu#v4       | CMU Cell Voltage 4 (V) / 1000 round 3  |
| cmu#v5       | CMU Cell Voltage 5 (V) / 1000 round 3  |
| cmu#v6       | CMU Cell Voltage 6 (V) / 1000 round 3  |
| cmu#v7       | CMU Cell Voltage 7 (V) / 1000 round 3  |


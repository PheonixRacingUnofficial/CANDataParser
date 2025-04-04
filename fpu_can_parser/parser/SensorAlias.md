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
| mppt1i        | MPPT1 Input                  |
| mppt1o        | MPPT1 Output                 |
| mppt1t        | MPPT1 Temperature            |
| mppt1aps      | MPPT1 Auxiliary Power Supply |
| mppt1l        | MPPT1 Limits                 |
| mppt1s        | MPPT1 Status                 |
| mppt1pc       | MPPT1 Power Connector        |
| mppt2i        | MPPT2 Input                  |
| mppt2o        | MPPT2 Output                 |
| mppt2t        | MPPT2 Temperature            |
| mppt2aps      | MPPT2 Auxiliary Power Supply |
| mppt2l        | MPPT2 Limits                 |
| mppt2s        | MPPT2 Status                 |
| mppt2pc       | MPPT2 Power Connector        |

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

### MPPT1 Data

| Abbreviation       | Description                           |
|--------------------|-------------------------------------|
| mppt1iv           | MPPT1 Input Voltage (V)             |
| mppt1ic           | MPPT1 Input Current (A)             |
| mppt1ov           | MPPT1 Output Voltage (V)            |
| mppt1oc           | MPPT1 Output Current (A)            |
| mppt1mt           | MPPT1 Mosfet Temperature (°C)       |
| mppt1ct           | MPPT1 Control Temperature (°C)      |
| mppt1_12v         | MPPT1 12V Supply Voltage (V)        |
| mppt1_3v          | MPPT1 3V Supply Voltage (V)         |
| mppt1mov          | MPPT1 Max Output Voltage (V)        |
| mppt1mic          | MPPT1 Max Input Current (A)         |
| mppt1canrxerrcnt  | MPPT1 CAN RX Error Count            |
| mppt1cantxerrcnt  | MPPT1 CAN TX Error Count            |
| mppt1cantxofcnt   | MPPT1 CAN TX Overflow Count         |
| mppt1errflg       | MPPT1 Error Flag                    |
| mppt1limflg       | MPPT1 Limit Flag                    |
| mppt1mode         | MPPT1 Mode                           |
| mppt1tstcnt       | MPPT1 Test Count                    |
| mppt1ovcon        | MPPT1 Output Voltage Connector      |
| mppt1ct           | MPPT1 Connector Temp                |

### MPPT2 Data

| Abbreviation       | Description                           |
|--------------------|-------------------------------------|
| mppt2iv           | MPPT2 Input Voltage (V)             |
| mppt2ic           | MPPT2 Input Current (A)             |
| mppt2ov           | MPPT2 Output Voltage (V)            |
| mppt2oc           | MPPT2 Output Current (A)            |
| mppt2mt           | MPPT2 Mosfet Temperature (°C)       |
| mppt2ct           | MPPT2 Control Temperature (°C)      |
| mppt2_12v         | MPPT2 12V Supply Voltage (V)        |
| mppt2_3v          | MPPT2 3V Supply Voltage (V)         |
| mppt2mov          | MPPT2 Max Output Voltage (V)        |
| mppt2mic          | MPPT2 Max Input Current (A)         |
| mppt2canrxerrcnt  | MPPT2 CAN RX Error Count            |
| mppt2cantxerrcnt  | MPPT2 CAN TX Error Count            |
| mppt2cantxofcnt   | MPPT2 CAN TX Overflow Count         |
| mppt2errflg       | MPPT2 Error Flag                    |
| mppt2limflg       | MPPT2 Limit Flag                    |
| mppt2mode         | MPPT2 Mode                           |
| mppt2tstcnt       | MPPT2 Test Count                    |
| mppt2ovcon        | MPPT2 Output Voltage Connector      |
| mppt2ct           | MPPT2 Connector Temp                |

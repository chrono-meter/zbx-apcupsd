# zbx-apcupsd
Zabbix Template for USB attached APC UPS

This template is pretty simple, it uses apcupsd to query the UPS over USB, and ingests that data into Zabbix.

Data collected:
- Battery Charge (%)
- Battery Voltage (V)
- Hi-Voltage Transfer Threshold (V)
- Lo-Voltage Transfer Threshold (V)
- Line Voltage (V)
- Minimum Battery Charge (Shutoff threshold) (%)
- Minimum Time on Battery Remaining (m)
- UPS State (status)
- Time Left on Battery (m)
- Current Load (W) (this value is imprecise, as it is calculated based off of the Load % and the nominal power rating (pulled from apcaccess and used as a macro))
- Model name
- Serial Number
- Battery Replacement Date

Triggers:
- Power interruption - Operating on battery
- UPS Recharging - Battery is charging
- Time Remaining Low - Macro specified threshold for alerting on a low battery
- Time Remaining Very Low - Macro specified threshold for alerting on a critically low battery
- 3/4/5 years gone after battery replacement

User Macros:
- {$APC_REM_WARN} - Time remaining on battery warning value, defaults to 10 minutes
- {$APC_REM_CRIT} - Time remaining on battery critical value, defaults to 3 minutes

Instructions:
1. Install `apcupsd` using your package manager.
2. `sudo wget https://github.com/chrono-meter/zbx-apcupsd/raw/main/apcaccess-json.py -O /etc/zabbix/zabbix_agent2.d/apcaccess-json.py`
3. `sudo chmod +x /etc/zabbix/zabbix_agent2.d/apcaccess-json.py`
4. `sudo wget https://github.com/chrono-meter/zbx-apcupsd/raw/main/userparameter_apcupsd.conf -O /etc/zabbix/zabbix_agent2.d/userparameter_apcupsd.conf`
5. `sudo systemctl restart zabbix-agent2.service`
6. Test by `zabbix_get -s 127.0.0.1 -p 10050 -k "apcupsd.apcaccess"`
7. Import the template XML.
8. Assign the template to your host.
9. Make sure macros are at values that work for you.

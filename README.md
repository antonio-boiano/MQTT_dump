# MQTT dump

### Prerequisites

- Ensure Python 3 is installed on your system.
- The following Python scripts should be present in the same directory as this Bash script:
  - `mqtt_acquire.py`
  - `mqtt_compress.py`
- Install_
  - `pip install paho-mqtt`
### Running the Script

To execute the Bash script, use the following command:

```bash
./mqtt_dump.sh max_size_mb delay_seconds parent_output_folder
```

### Kill the Script

To kill dump execute:

```bash
./kill_dump.sh
```

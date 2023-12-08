import paho.mqtt.client as mqtt
import json
import csv
import time
import zlib
import argparse
import os

current_file_size = 0
file_count = 1

def save_to_split_csv(mqtt_info_dict, start_time, host, port, saving_folder, max_file_size_mb=100):
    global current_file_size, file_count
    file_prefix = f"mqtt_dump_{start_time}_{host}_{port}"
    file_extension = ".csv"
    max_file_size_bytes = max_file_size_mb * 1024 * 1024  # Convert MB to bytes

    def open_file():
        return open(os.path.join(saving_folder, f"{file_prefix}_{file_count}{file_extension}"), "a", newline='')

        
    def create_new_file():
        global current_file_size, file_count
        current_file_size = 0
        file_count += 1
        print(f"Creating new file: {file_prefix}_{file_count}{file_extension}")
        return open(os.path.join(saving_folder, f"{file_prefix}_{file_count}{file_extension}"), "a", newline='')

        
    def write_to_file(csv_file):
        csv_writer = csv.DictWriter(csv_file, fieldnames=mqtt_info_dict.keys())

        if os.path.getsize(csv_file.name) == 0:
            csv_writer.writeheader()

        csv_writer.writerow(mqtt_info_dict)

    current_file = open_file()

    if current_file_size >= max_file_size_bytes:
        current_file.close()
        current_file = create_new_file()

    write_to_file(current_file)
    current_file_size = os.path.getsize(current_file.name)


    current_file.close()



# Create a dictionary to store information
mqtt_info_dict = {
    "Timestamp": None,
    "Topic": None,
    "QoS": None,
    "Retain": None,
    "DUP":None,
    "Message ID": None,
    "Payload Length": None,
    "Payload JSON": None,
    "JSON Type": None,
    "Payload Content": None
}
start_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())
def parse_args():
    parser = argparse.ArgumentParser(description="MQTT Subscriber with Payload Analysis")
    parser.add_argument("--host", default="test.mosquitto.org", help="MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--topic", default="#", help="MQTT topic to subscribe to")
    parser.add_argument("--maxsize", type=int, default=100, help="Max size in MB of each CSV file")
    parser.add_argument("-c", "--compress", action="store_true", help="Enable compression of the payload")
    parser.add_argument("--savedir", default="", help="Folder path to save CSV files (default: current working directory)")
    return parser.parse_args()

# Callback when a connection is established with the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribe to the specified topic
    client.subscribe(args.topic, qos=2)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    #print(msg)
    # Extract MQTT header information
    mqtt_info_dict["Timestamp"] = msg.timestamp #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    mqtt_info_dict["Topic"] = str(msg.topic)
    mqtt_info_dict["QoS"] = msg.qos
    mqtt_info_dict["Retain"] = msg.retain
    mqtt_info_dict["DUP"] = msg.dup
    mqtt_info_dict["Message ID"] = msg.mid
    mqtt_info_dict["Payload Length"] = len(msg.payload)

    # Check if the payload is JSON
    try:
        payload_dec = msg.payload.decode('utf-8')
        json_payload = json.loads(payload_dec)
        mqtt_info_dict["Payload JSON"] = 1
        mqtt_info_dict["JSON Type"] = type(json_payload)

    except:
        mqtt_info_dict["Payload JSON"] = 0
        mqtt_info_dict["JSON Type"] = None
            # Compress the payload if the compress flag is set
    if args.compress:
        compressed_payload = zlib.compress(msg.payload[:40])
        mqtt_info_dict["Payload Content"] = compressed_payload
    else:
        mqtt_info_dict["Payload Content"] = str(msg.payload[:40])
    
    save_to_split_csv(mqtt_info_dict, start_time, args.host, args.port, args.savedir, max_file_size_mb=args.maxsize)


# Parse command-line arguments
args = parse_args()

# Create an MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the specified MQTT broker
client.connect(args.host, args.port, 60)

print("MQTT service started and running...")


# Loop to keep the script running
client.loop_forever()

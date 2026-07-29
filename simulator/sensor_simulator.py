import paho.mqtt.client as mqtt
import json
import time
import random
import os

# Load environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "shelly/sim/device_01")

# Create MQTT Client
client = mqtt.Client(client_id="shelly-simulator")

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT broker, result code: {rc}")

client.on_connect = on_connect
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()

print(f"📡 Shelly Simulator Started. Publishing to topic: {MQTT_TOPIC}")

# Continuous generate simulated Shelly sensor data
while True:
    sensor_data = {
        "timestamp": round(time.time()),
        "temp_c": round(random.uniform(21.0, 29.5), 2),
        "power_watts": round(random.uniform(3, 140), 2),
        "total_energy_kwh": round(random.uniform(0.01, 4.5), 3),
        "online": True
    }
    payload = json.dumps(sensor_data)
    client.publish(MQTT_TOPIC, payload)
    print(f"📤 Publish data: {payload}")
    time.sleep(5)

import json, os
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

print(f"Using DB: {DB_NAME}")
mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = mongo_client[DB_NAME]
collection = db["sensor"]
print("MongoDB ready - collection 'sensor'")

def on_connect(client, userdata, flags, rc):
    print(f"MQTT Connected with code {rc}")
    if rc == 0:
        client.subscribe("pabrik/sensor/suhu")
        print("✓ Subscribed to pabrik/sensor/suhu")
    else:
        print(f"✗ Connection failed: {rc}")

def on_message(client, userdata, msg):
    try:
        print(f"Message on {msg.topic}: {msg.payload.decode()}")
        payload = json.loads(msg.payload.decode())
        payload['timestamp'] = datetime.fromisoformat(payload['timestamp'])
        result = collection.insert_one(payload)
        print(f"✓ Saved to MongoDB ID: {result.inserted_id} | {payload['mesin']} {payload['suhu']}°C")
    except Exception as e:
        print(f"✗ Message error: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("Connecting to broker.hivemq.com (120s timeout)...")
mqtt_client.connect("broker.hivemq.com", 1883, 120)
mqtt_client.loop_forever()

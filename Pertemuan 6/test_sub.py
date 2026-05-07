import json, os
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
print(f"Mongo URI loaded: {os.getenv('MONGO_URI')[:20]}...")
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client[os.getenv("DB_NAME")]
collection = db["sensor"]
print("DB collection ready")

def on_connect(client, userdata, flags, rc):
    print(f"MQTT Connected with result code {rc}")
    if rc == 0:
        client.subscribe("pabrik/sensor/suhu")
        print("Subscribed to topic")
    else:
        print("Failed to connect to broker!")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Received: {payload}")
        payload['timestamp'] = datetime.fromisoformat(payload['timestamp'])
        result = collection.insert_one(payload)
        print(f"[MONGO OK] Inserted ID: {result.inserted_id}")
    except Exception as e:
        print(f"[MESSAGE ERROR] {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("Connecting to MQTT broker...")
mqtt_client.connect("broker.hivemq.com", 1883, 120)
mqtt_client.loop_forever()

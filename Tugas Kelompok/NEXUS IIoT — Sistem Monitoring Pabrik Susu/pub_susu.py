import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT", 34423))
TOPIC = os.getenv("MQTT_TOPIC")
USERNAME = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASS")


def generate_sensor_data(area, probabilitas_bahaya=0.05):
    data = {"timestamp": datetime.utcnow().isoformat(), "area": area}
    is_anomaly = random.random() < probabilitas_bahaya

    if area == "Tangki Susu Utama":
        data["suhu"] = round(random.uniform(9.0, 12.0) if is_anomaly else random.uniform(2.0, 6.0), 1)
        data["pressure"] = round(random.uniform(4.5, 6.0) if is_anomaly else random.uniform(1.0, 3.0), 1)
        data["level"] = round(random.uniform(96, 100) if is_anomaly else random.uniform(30, 90), 1)
        data["ph"] = round(random.uniform(5.5, 6.2) if is_anomaly else random.uniform(6.5, 6.8), 1)
    
    elif area == "Jalur Pasteurisasi":
        data["suhu"] = round(random.uniform(50.0, 64.0) if is_anomaly else random.uniform(70.0, 75.0), 1)
        data["flow_rate"] = round(random.uniform(5.0, 14.0) if is_anomaly else random.uniform(20.0, 40.0), 1)
        data["pressure"] = round(random.uniform(5.5, 7.0) if is_anomaly else random.uniform(2.0, 4.0), 1)
        
    elif area == "Ruang Pendingin":
        data["suhu"] = round(random.uniform(9.0, 15.0) if is_anomaly else random.uniform(2.0, 5.0), 1)
        data["kelembapan"] = round(random.uniform(85, 95) if is_anomaly else random.uniform(40, 70), 1)
        
    elif area == "Area Filling":
        data["flow_rate"] = round(random.uniform(2.0, 9.0) if is_anomaly else random.uniform(15.0, 35.0), 1)
        data["pressure"] = round(random.uniform(5.5, 7.0) if is_anomaly else random.uniform(2.0, 4.0), 1)
        data["suhu"] = round(random.uniform(11.0, 15.0) if is_anomaly else random.uniform(4.0, 8.0), 1)
        
    elif area == "Tangki Fermentasi":
        data["suhu"] = round(random.uniform(46.0, 50.0) if is_anomaly else random.uniform(35.0, 43.0), 1)
        data["ph"] = round(random.uniform(3.0, 3.7) if is_anomaly else random.uniform(4.0, 4.6), 1)
        data["level"] = round(random.uniform(96, 100) if is_anomaly else random.uniform(30, 90), 1)

    return data

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT, 60)

areas = ["Tangki Susu Utama", "Jalur Pasteurisasi", "Ruang Pendingin", "Area Filling", "Tangki Fermentasi"]

print("Memulai simulasi Pabrik Susu...")
try:
    while True:
        for area in areas:
            payload = generate_sensor_data(area)
            client.publish(TOPIC, json.dumps(payload))
            print(f"[PUBLISHED] {area}: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nSimulasi dihentikan.")
    client.disconnect()
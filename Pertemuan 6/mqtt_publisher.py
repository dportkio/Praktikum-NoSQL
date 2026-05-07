import json, time, random
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "pabrik/sensor/suhu"

client = mqtt.Client()
client.connect(BROKER, PORT, 120)
client.loop_start()

while True:
    data = {
        "mesin": f"CNC-{random.randint(1,5):02d}",
        "suhu": round(random.uniform(60, 100), 2),
        "getaran": round(random.uniform(0.1, 0.5), 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    payload = json.dumps(data)
    client.publish(TOPIC, payload)
    print(f"[PUB] {payload}")
    time.sleep(2)

import json, time, random
import paho.mqtt.client as mqtt
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    print(f"Publisher connected: {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.hivemq.com", 1883, 120)
client.loop_start()
time.sleep(2)

for i in range(3):
    data = {
        "mesin": f"CNC-{random.randint(1,3):02d}",
        "suhu": round(random.uniform(70, 95), 2),
        "getaran": round(random.uniform(0.1, 0.4), 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    result = client.publish("pabrik/sensor/suhu", json.dumps(data))
    print(f"Published (rc={result.rc}): {data}")
    time.sleep(3)

print("Test complete")

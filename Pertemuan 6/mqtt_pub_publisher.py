import json
import random
import time
import paho.mqtt.client as mqtt

# --- KONFIGURASI ---
# Konfigurasi MQTT
broker = "170.106.137.233"
port = 34423
topic = "subpub"
username = "kel1" 
password = "apaan" 


client_id = f"pub-{int(time.time())}-{random.randint(1000, 9999)}"
client = mqtt.Client(client_id=client_id, clean_session=True)

batches = [f"BATCH-{i:03d}" for i in range(1, 21)]
mesins = ["CNC-01", "CNC-02", "LAS-01", "PRESS-01", "PAINT-01"]

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Publisher connected to MQTT broker (rc={rc})")
    else:
        print(f"❌ Connection failed, result code: {rc}")

def on_publish(client, userdata, mid):
    print(f"📤 Publish acknowledged (mid={mid})")

# ========================================================
# WAJIB: Set username & password SEBELUM connect
# ========================================================
client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_publish = on_publish

print(f"Connecting to {broker}:{port} as client_id={client_id} ...")

try:
    client.connect(broker, port, keepalive=60)
    client.loop_start()

    while True:
        payload = {
            "batch": random.choice(batches),
            "mesin": random.choice(mesins),
            "jumlah": random.randint(100, 500),
            "reject": random.randint(0, 50),
        }

        # Pastikan reject tidak lebih dari jumlah
        if payload["reject"] > payload["jumlah"]:
            payload["reject"] = payload["jumlah"]

        payload_json = json.dumps(payload)

        # QoS 1 biar lebih pasti sampe
        info = client.publish(topic, payload_json, qos=1)
        
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"❌ Publish failed (rc={info.rc}) payload={payload}")
        else:
            print(f"Published to {topic}: {payload}")

        time.sleep(3)

except KeyboardInterrupt:
    print("Stopping publisher...")
finally:
    client.loop_stop()
    client.disconnect()
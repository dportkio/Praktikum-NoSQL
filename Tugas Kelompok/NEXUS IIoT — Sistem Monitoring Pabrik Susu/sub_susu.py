import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# =========================================
# KONFIGURASI MONGODB DARI .ENV
# =========================================
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 948))
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_AUTH_DB = os.getenv("MONGO_AUTH_DB")

DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_MONITORING = "monitoring_susu"
COLLECTION_ALERT = "alert"

MONGO_URI = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}"
    f"@{MONGO_HOST}:{MONGO_PORT}/"
    f"?authSource={MONGO_AUTH_DB}"
)

# =========================================
# KONFIGURASI MQTT DARI .ENV
# =========================================
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 34423))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

MQTT_USERNAME = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASS")

MQTT_KEEPALIVE = 60

# =========================================
# THRESHOLD SENSOR
# =========================================

THRESHOLD = {

    "Tangki Susu Utama": {
        "suhu_max": 8,
        "pressure_max": 4,
        "ph_min": 6.3,
        "level_max": 95
    },

    "Jalur Pasteurisasi": {
        "suhu_min": 65,
        "flow_rate_min": 15
    },

    "Ruang Pendingin": {
        "suhu_max": 8
    }
}

# =========================================
# KONEKSI MONGODB
# =========================================

try:
    mongo_client = MongoClient(MONGO_URI)

    mongo_client.admin.command("ping")

    print("[MONGODB] Berhasil terhubung ke MongoDB Server.")

except Exception as e:
    print(f"[MONGODB ERROR] {e}")
    exit()

db = mongo_client[DATABASE_NAME]

col_monitoring = db[COLLECTION_MONITORING]
col_alert = db[COLLECTION_ALERT]

# =========================================
# CEK ANOMALI
# =========================================

def save_alert(data, jenis, pesan):

    alert_doc = {
        "timestamp": data.get("timestamp", datetime.now().isoformat()),
        "area": data["area"],
        "jenis_alert": jenis,
        "nilai": data[jenis],
        "status": "Bahaya",
        "pesan": pesan
    }

    col_alert.insert_one(alert_doc)

    print("=" * 50)
    print("[!!! ALERT BAHAYA !!!]")
    print(f"Area   : {data['area']}")
    print(f"Jenis  : {jenis}")
    print(f"Nilai  : {data[jenis]}")
    print(f"Pesan  : {pesan}")
    print("=" * 50)

def check_anomaly(data):

    area = data.get("area")

    if area not in THRESHOLD:
        return

    config = THRESHOLD[area]

    # =====================================
    # Tangki Susu Utama
    # =====================================

    if "suhu_max" in config:
        if data.get("suhu", 0) > config["suhu_max"]:
            save_alert(data, "suhu", "Suhu terlalu tinggi!")

    if "pressure_max" in config:
        if data.get("pressure", 0) > config["pressure_max"]:
            save_alert(data, "pressure", "Tekanan terlalu tinggi!")

    if "ph_min" in config:
        if data.get("ph", 7) < config["ph_min"]:
            save_alert(data, "ph", "pH susu abnormal!")

    if "level_max" in config:
        if data.get("level", 0) > config["level_max"]:
            save_alert(data, "level", "Tangki hampir overflow!")

    # =====================================
    # Jalur Pasteurisasi
    # =====================================

    if "suhu_min" in config:
        if data.get("suhu", 100) < config["suhu_min"]:
            save_alert(data, "suhu", "Suhu pasteurisasi terlalu rendah!")

    if "flow_rate_min" in config:
        if data.get("flow_rate", 100) < config["flow_rate_min"]:
            save_alert(data, "flow_rate", "Aliran susu terlalu rendah!")

# =========================================
# MQTT CALLBACK
# =========================================

def on_connect(client, userdata, flags, rc, properties=None):

    if rc == 0:

        print("[MQTT] Berhasil terhubung ke broker.")

        client.subscribe(MQTT_TOPIC)

        print(f"[MQTT] Subscribe topic: {MQTT_TOPIC}")

    else:

        print(f"[MQTT ERROR] Gagal connect. RC = {rc}")

def on_disconnect(client, userdata, rc, properties=None):

    print("[MQTT] Terputus dari broker.")

def on_message(client, userdata, msg):

    try:

        payload = msg.payload.decode()

        data = json.loads(payload)

        # fallback timestamp
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()

        # simpan data monitoring
        col_monitoring.insert_one(data.copy())

        print(f"[SAVED] Data area {data['area']} tersimpan.")

        # cek anomaly
        check_anomaly(data)

    except Exception as e:

        print(f"[ERROR] Gagal memproses data: {e}")

# =========================================
# MQTT CLIENT
# =========================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# =========================================
# CONNECT MQTT
# =========================================

try:

    client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        MQTT_KEEPALIVE
    )

    client.loop_forever()

except Exception as e:

    print(f"[MQTT CONNECTION ERROR] {e}")
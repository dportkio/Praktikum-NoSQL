import json
import time
import os
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env kalau lu mau simpen password di file .env (Sangat disarankan!)
load_dotenv()

# Konfigurasi MQTT
broker = "170.106.137.233"
port = 34423
topic = "subpub"
username = "kel1" 
password = "apaan" 

# MongoDB 
try:
    client_mongo = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
    client_mongo.admin.command('ping')
    db = client_mongo['mqtt_db']
    collection = db['produksi_mqtt']
    print("✅ MongoDB terhubung!")
except Exception as e:
    print(f"❌ MongoDB tidak terhubung. Error: {e}")
    collection = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Berhasil konek ke broker (Result Code: {rc})")
        client.subscribe(topic)
    else:
        print(f"❌ Gagal konek, kode respon: {rc}")

def on_message(client, userdata, msg):
    print(f"📥 Masuk: topic={msg.topic} payload={msg.payload!r}")
    try:
        payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print("Bukan format JSON, diabaikan.")
        return

    # Pake timezone.utc biar sinkron sama database
    payload['timestamp'] = datetime.now(timezone.utc)
    
    # Kalkulasi Reject Rate buat monitoring produksi
    jumlah = payload.get('jumlah', 0)
    reject = payload.get('reject', 0)
    reject_rate = (reject / jumlah * 100) if jumlah else 0
    payload['reject_rate'] = round(reject_rate, 2)

    if reject_rate > 5:
        payload['peringatan'] = True
        print(f"⚠️ Warning: Reject rate {payload['reject_rate']}% di {payload.get('mesin')}")
    else:
        payload['peringatan'] = False

    # if collection:
    #     collection.insert_one(payload)
    #     print(f"💾 Tersimpan ke MongoDB")

# Inisialisasi Client
client = mqtt.Client()

# ========================================================
# WAJIB: Pasang username & password SEBELUM connect()
# ========================================================
client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_message = on_message

print(f"Menghubungkan ke {broker}...")
client.connect(broker, port)

print(f"Subscriber listening to {topic}...")
client.loop_forever()
from datetime import datetime
import os
from pydoc import doc
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
# atau gunakan MONGO_URI
db = client["database_test"]
collection = db["koleksi_test"]

try:
    client.admin.command('ping')
    print("Koneksi berhasil!")
except Exception as e:
    print("Gagal:", e)


from datetime import datetime, timezone
# Insert satu dokumen
sensor_data = {
    "mesin": "CNC-01",
    "suhu": 72.5,
    "getaran": 0.13,
    "timestamp": datetime.now(timezone.utc)
}
result = collection.insert_one(sensor_data)
print(result.inserted_id)

# Insert banyak dokumen sekaligus
docs = [
    {"mesin": "CNC-01", "suhu": 71.0, "timestamp": datetime.utcnow()},
    {"mesin": "CNC-02", "suhu": 85.3, "timestamp": datetime.utcnow()}
]
result = collection.insert_many(docs)

# Semua dokumen mesin CNC-01, hanya tampilkan suhu dan timestamp
cursor = collection.find(
    {"mesin": "CNC-02"},
    {"_id": 0, "suhu": 1, "timestamp": 1}
).sort("timestamp", -1).limit(10)

for doc in cursor:
    print(doc)


# Menambah jumlah reject satu mesin
collection.update_many(
    {"mesin": "CNC-02"},
    {"$inc": {"reject_count": 1}, "$set": {"status": "Baru"}}
)

# Menambahkan field baru jika belum ada, atau update jika sudah ada
collection.update_one(
    {"mesin": "CNC-05"},
    {"$set": {"suhu": 80.0, "timestamp": datetime.utcnow(), "status": "Baru"}},
    upsert=True
)

# Hapus dokumen yang lebih lama dari 1 Januari 2026
collection.delete_many({"timestamp": {"$lt": datetime(2026,1,1)}})

# Proses data dengan batch
def process(doc):
    # Simulasi proses data
    print(f"Memproses data dari mesin {doc['mesin']} dengan suhu {doc['suhu']} pada {doc['timestamp']}")
cursor = collection.find().batch_size(500)
for doc in cursor:
    process(doc)

# Agregasi untuk menghitung suhu maksimum per mesin yang melebihi 80 derajat
pipeline = [
    {"$match": {"suhu": {"$gt": 80}}},
    {"$group": {"_id": "$mesin", "max_suhu": {"$max": "$suhu"}}}
]
results = collection.aggregate(pipeline)
for r in results:
    print(r)


# Menggunakan pandas untuk analisis data
import pandas as pd

cursor = collection.find({"mesin": "CNC-01"})
df = pd.DataFrame(list(cursor))
print(df.head())
print(df.describe())

import matplotlib.pyplot as plt
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
df['suhu'].plot()
plt.show()


# Simulasi data sensor yang terus masuk setiap beberapa detik
import time
import random
from datetime import datetime

while True:
    doc = {
        "mesin": f"CNC-{random.randint(1,5):02d}",
        "suhu": round(random.uniform(60, 100), 2),
        "getaran": round(random.uniform(0.1, 0.5), 2),
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(doc)
    print("Inserted:", doc)
    time.sleep(2)  # setiap 2 detik


# Menambahkan logging untuk memantau proses insert
import logging
logging.basicConfig(level=logging.INFO)

try:
    collection.insert_one(doc)
    logging.info("Data inserted")
except Exception as e:
    logging.error(f"Insert gagal: {e}")
# from dotenv import load_dotenv
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# import random, os

# load_dotenv()
# client = MongoClient(os.getenv("MONGO_URI"))
# db = client[os.getenv("DB_NAME")]
# collection = db["sensor"]

# data = []
# for i in range(10):
#     doc = {
#         "mesin": f"CNC-{random.randint(1,3):02d}",
#         "suhu": round(random.uniform(60, 100), 2),
#         "getaran": round(random.uniform(0.1, 0.5), 2),
#         "timestamp": datetime.utcnow() - timedelta(minutes=i*5),
#         "status": "normal"
#     }
#     data.append(doc)
# result = collection.insert_many(data)
# print(f"Tersimpan {len(result.inserted_ids)} dokumen")


# cursor = collection.find(
#     {"mesin": "CNC-01"},
#     {"_id": 0, "suhu": 1, "timestamp": 1}
# ).sort("timestamp", -1).limit(5)
# print("Data CNC-01 terbaru:")
# for doc in cursor:
#     print(doc)

#     update_result = collection.update_many(
#     {"suhu": {"$gt": 90}},
#     {"$set": {"status": "maintenance"}}
# )
# print(f"Update: {update_result.modified_count} dokumen diubah")

# satu_jam_lalu = datetime.utcnow() - timedelta(hours=1)
# delete_result = collection.delete_many({"timestamp": {"$lt": satu_jam_lalu}})
# print(f"Delete: {delete_result.deleted_count} dokumen dihapus")

# satu_jam_lalu = datetime.utcnow() - timedelta(hours=1)
# delete_result = collection.delete_many({"timestamp": {"$lt": satu_jam_lalu}})
# print(f"Delete: {delete_result.deleted_count} dokumen dihapus")

# import
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
import random, os

# module 
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["sensor"]

# logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crud_sensor.log"),
        logging.StreamHandler()
    ]
)
try:
    result = collection.insert_many(data)
    logging.info(f"Insert berhasil, {len(result.inserted_ids)} dokumen")
except Exception as e:
    logging.error(f"Insert gagal: {e}")

# Insert data sensor acak
data = []
for i in range(10):
    doc = {
        "mesin": f"CNC-{random.randint(1,3):02d}",
        "suhu": round(random.uniform(60, 100), 2),
        "getaran": round(random.uniform(0.1, 0.5), 2),
        "timestamp": datetime.utcnow() - timedelta(minutes=i*5),
        "status": "normal"
    }
    data.append(doc)
result = collection.insert_many(data)
print(f"Tersimpan {len(result.inserted_ids)} dokumen")

# Baca data CNC-01 terbaru
cursor = collection.find(
    {"mesin": "CNC-01"},
    {"_id": 0, "suhu": 1, "timestamp": 1}
).sort("timestamp", -1).limit(5)
print("Data CNC-01 terbaru:")
for doc in cursor:
    print(doc)

# Update status menjadi "maintenance" jika suhu > 90
update_result = collection.update_many(
    {"suhu": {"$gt": 90}},
    {"$set": {"status": "maintenance"}}
)
print(f"Update: {update_result.modified_count} dokumen diubah")

# Hapus data yang lebih lama dari 1 jam
# satu_jam_lalu = datetime.utcnow() - timedelta(hours=1)
# delete_result = collection.delete_many({"timestamp": {"$lt": satu_jam_lalu}})
# print(f"Delete: {delete_result.deleted_count} dokumen dihapus")


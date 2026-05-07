import time, random
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["sensor"]

while True:
    doc = {
        "mesin": f"CNC-{random.randint(1,5):02d}",
        "suhu": round(random.uniform(60, 100), 2),
        "getaran": round(random.uniform(0.1, 0.5), 2),
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(doc)
    print(f"[{datetime.utcnow()}] Inserted: {doc['mesin']} - {doc['suhu']}°C")
    time.sleep(2)
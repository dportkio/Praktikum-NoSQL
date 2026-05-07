from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# =============================
# KONEKSI MONGODB
# =============================
client = MongoClient("mongodb://localhost:27017")
db = client["studi_kasus"]
collection = db["produksi_harian"]

# reset collection
collection.drop()

# =============================
# SETUP DATA
# =============================
mesin_list = [f"M{i:02d}" for i in range(1, 11)]
shift_list = [1, 2, 3]

start_date = datetime(2026, 1, 1)

docs = []

# =============================
# GENERATE DATA
# =============================
for i in range(250):  # > 200 dokumen
    mesin = random.choice(mesin_list)

    tanggal = start_date + timedelta(days=random.randint(0, 90))

    shift = random.choice(shift_list)

    target = random.randint(200, 500)

    # performance
    actual_ok = int(target * random.uniform(0.6, 1.0))
    actual_reject = int(actual_ok * random.uniform(0.0, 0.15))

    durasi_tersedia = 480
    durasi_operasi = int(durasi_tersedia * random.uniform(0.7, 1.0))

    doc = {
        "mesin": mesin,
        "tanggal": tanggal,
        "shift": shift,
        "target": target,
        "actual_ok": actual_ok,
        "actual_reject": actual_reject,
        "durasi_operasi_menit": durasi_operasi,
        "durasi_tersedia_menit": durasi_tersedia
    }

    docs.append(doc)

# =============================
# INSERT KE DB
# =============================
collection.insert_many(docs)

print("✅ Data berhasil diinsert:", collection.count_documents({}))
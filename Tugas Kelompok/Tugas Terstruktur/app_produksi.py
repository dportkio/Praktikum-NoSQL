import os
import logging
from datetime import datetime
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# ==========================================
# 1. KONFIGURASI LOGGING
# ==========================================
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==========================================
# 2. SETUP KONEKSI DATABASE
# ==========================================
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "latihan_industri") # Sesuaikan nama DB kalau beda

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    collection = db['produksi']
    logging.info("Aplikasi dimulai. Koneksi MongoDB sukses.")
except Exception as e:
    print("❌ Gagal terhubung ke database. Pastikan MongoDB berjalan!")
    logging.error(f"Koneksi DB Gagal: {e}")
    exit()

# ==========================================
# 3. FUNGSI-FUNGSI MODULAR
# ==========================================

def input_data():
    print("\n--- 1. INPUT DATA PRODUKSI BARU ---")
    try:
        batch = input("Masukkan Batch (contoh: BATCH-001): ").upper()
        mesin = input("Masukkan Mesin (contoh: CNC-01): ").upper()
        jumlah = int(input("Masukkan Jumlah Produksi: "))
        reject = int(input("Masukkan Jumlah Reject: "))
        tanggal_str = input("Masukkan Tanggal (YYYY-MM-DD): ")
        
        # Konversi string ke object datetime
        tanggal = datetime.strptime(tanggal_str, "%Y-%m-%d")

        doc = {
            "batch": batch,
            "mesin": mesin,
            "jumlah": jumlah,
            "reject": reject,
            "tanggal": tanggal
        }
        
        collection.insert_one(doc)
        print("✅ Data berhasil disimpan ke MongoDB!")
        logging.info(f"Insert berhasil: Batch {batch} di {mesin} ({jumlah} pcs)")
        
    except ValueError as e:
        print("❌ Input tidak valid! Pastikan angka dan format tanggal benar.")
        logging.error(f"Error input data (ValueError): {e}")
    except Exception as e:
        print("❌ Terjadi kesalahan saat menyimpan data.")
        logging.error(f"Insert gagal: {e}")

def tampilkan_data_mesin():
    print("\n--- 2. TAMPILKAN DATA PER MESIN ---")
    mesin = input("Masukkan Nama Mesin: ").upper()
    try:
        # Tarik data dari Mongo, sembunyikan _id biar tabelnya bersih
        cursor = collection.find({"mesin": mesin}, {"_id": 0})
        data = list(cursor)
        
        if not data:
            print(f"⚠️ Tidak ada data produksi untuk mesin {mesin}.")
            logging.info(f"Query data {mesin}: 0 hasil.")
            return
            
        df = pd.DataFrame(data)
        # Ubah format tanggal di pandas biar enak dibaca pas di print
        df['tanggal'] = df['tanggal'].dt.strftime('%Y-%m-%d')
        print("\n", df.to_string(index=False))
        logging.info(f"Query data {mesin}: Menampilkan {len(data)} baris.")
        
    except Exception as e:
        print("❌ Terjadi kesalahan.")
        logging.error(f"Query mesin {mesin} gagal: {e}")

def hitung_reject_rate():
    print("\n--- 3. BATCH DENGAN REJECT RATE > 5% ---")
    
    # Agregasi untuk menghitung (reject/jumlah) * 100
    pipeline = [
        {"$match": {"jumlah": {"$gt": 0}}}, # Hindari error division by zero
        {"$project": {
            "_id": 0,
            "batch": 1,
            "mesin": 1,
            "jumlah": 1,
            "reject": 1,
            "tanggal": { "$dateToString": { "format": "%Y-%m-%d", "date": "$tanggal" } },
            "reject_rate": {
                "$multiply": [{"$divide": ["$reject", "$jumlah"]}, 100]
            }
        }},
        {"$match": {"reject_rate": {"$gt": 5}}}, # Filter yang di atas 5%
        {"$sort": {"reject_rate": -1}} # Urutkan dari yang paling parah
    ]
    
    try:
        results = list(collection.aggregate(pipeline))
        if not results:
            print("✅ Kinerja bagus! Tidak ada batch dengan reject rate di atas 5%.")
            logging.info("Query reject rate > 5%: 0 hasil ditemukan.")
            return
            
        df = pd.DataFrame(results)
        df['reject_rate'] = df['reject_rate'].round(2).astype(str) + '%'
        print("\n", df.to_string(index=False))
        logging.info(f"Query reject rate: {len(results)} batch bermasalah ditemukan.")
        
    except Exception as e:
        print("❌ Terjadi kesalahan saat menghitung agregasi.")
        logging.error(f"Agregasi reject rate gagal: {e}")

def ekspor_laporan():
    print("\n--- 4. EKSPOR LAPORAN BULANAN ---")
    bulan_tahun = input("Masukkan Bulan dan Tahun (MM-YYYY): ")
    try:
        bulan, tahun = map(int, bulan_tahun.split('-'))
        
        # Bikin rentang waktu awal bulan sampai awal bulan depan
        start_date = datetime(tahun, bulan, 1)
        if bulan == 12:
            end_date = datetime(tahun + 1, 1, 1)
        else:
            end_date = datetime(tahun, bulan + 1, 1)

        pipeline = [
            {"$match": {"tanggal": {"$gte": start_date, "$lt": end_date}}},
            {"$group": {
                "_id": "$mesin",
                "total_jumlah": {"$sum": "$jumlah"},
                "total_reject": {"$sum": "$reject"}
            }},
            {"$sort": {"_id": 1}} # Urutkan sesuai abjad mesin
        ]
        
        results = list(collection.aggregate(pipeline))
        if not results:
            print(f"⚠️ Tidak ada data produksi di bulan {bulan_tahun}.")
            logging.info(f"Ekspor laporan {bulan_tahun}: 0 data ditemukan.")
            return

        df = pd.DataFrame(results)
        df.rename(columns={"_id": "mesin"}, inplace=True)
        
        filename = f"laporan_{bulan_tahun}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Laporan berhasil diekspor menjadi: {filename}")
        logging.info(f"Ekspor sukses: {filename} ({len(results)} data mesin)")
        
    except ValueError:
        print("❌ Format input salah! Gunakan MM-YYYY (contoh: 05-2026).")
        logging.error("Ekspor gagal: Kesalahan format MM-YYYY.")
    except Exception as e:
        print("❌ Terjadi kesalahan saat mengekspor laporan.")
        logging.error(f"Ekspor laporan gagal: {e}")

# ==========================================
# 4. MENU UTAMA (LOOP)
# ==========================================
def main_menu():
    while True:
        print("\n" + "="*35)
        print("   SISTEM MANAJEMEN PRODUKSI")
        print("="*35)
        print("1. Input Data Produksi Baru")
        print("2. Tampilkan Data per Mesin")
        print("3. Cek Batch Reject Rate Tinggi (>5%)")
        print("4. Ekspor Laporan Bulanan (CSV)")
        print("5. Keluar")
        print("="*35)
        
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == '1':
            input_data()
        elif pilihan == '2':
            tampilkan_data_mesin()
        elif pilihan == '3':
            hitung_reject_rate()
        elif pilihan == '4':
            ekspor_laporan()
        elif pilihan == '5':
            print("Keluar dari aplikasi. Sampai jumpa!")
            logging.info("Aplikasi ditutup oleh pengguna.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1-5.")

if __name__ == "__main__":
    main_menu()
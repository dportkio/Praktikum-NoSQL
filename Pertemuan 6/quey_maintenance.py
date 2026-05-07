import pandas as pd
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['latihan6']
collection = db['maintenance']


print("=" * 70)
print("1. MENCARI DOKUMEN DENGAN BIAYA LEBIH DARI 1.000.000")
print("=" * 70)

# Cari dokumen dengan biaya > 1.000.000
query_high_cost = collection.find({"biaya": {"$gt": 1000000}})
high_cost_data = list(query_high_cost)

if high_cost_data:
    df_high_cost = pd.DataFrame(high_cost_data)
    # Hapus kolom _id jika ingin tampilan lebih rapi
    if '_id' in df_high_cost.columns:
        df_high_cost = df_high_cost.drop('_id', axis=1)
    print(f"\nDitemukan {len(high_cost_data)} dokumen:")
    print(df_high_cost.to_string(index=False))
else:
    print("\nTidak ada dokumen dengan biaya > 1.000.000")

print("\n" + "=" * 70)
print("2. UPDATE DOKUMEN DENGAN MESIN = 'CNC-01' DAN BIAYA = 1200000")
print("=" * 70)

# Update dokumen
update_result = collection.update_many(
    {"mesin": "CNC-01", "biaya": 1200000},
    {"$set": {"teknisi": "Dewi"}}
)

print(f"\nDokumen yang cocok: {update_result.matched_count}")
print(f"Dokumen yang diupdate: {update_result.modified_count}")

print("\n" + "=" * 70)
print("3. MENGHITUNG TOTAL BIAYA PER BULAN (AGGREGATION PIPELINE)")
print("=" * 70)

# Aggregation pipeline untuk total biaya per bulan
pipeline = [
    {
        "$group": {
            "_id": {
                "$dateToString": {
                    "format": "%Y-%m",
                    "date": "$tanggal"
                }
            },
            "total_biaya": {"$sum": "$biaya"}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

# Eksekusi aggregation
result_aggregation = list(collection.aggregate(pipeline))

if result_aggregation:
    df_monthly = pd.DataFrame(result_aggregation)
    df_monthly.columns = ['Bulan', 'Total Biaya']
    print("\nTotal Biaya per Bulan:")
    print(df_monthly.to_string(index=False))
    print(f"\nTotal keseluruhan: Rp {df_monthly['Total Biaya'].sum():,.0f}")
else:
    print("\nTidak ada data untuk aggregation")

client.close()
print("\n" + "=" * 70)
print("Selesai")
print("=" * 70)

import pandas as pd
from pymongo import MongoClient

# Baca file CSV menggunakan pandas
df = pd.read_csv('maintenance.csv')

# Konversi kolom tanggal menjadi tipe datetime
df['tanggal'] = pd.to_datetime(df['tanggal'])

# Hubungkan ke MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['latihan6']
collection = db['maintenance']

# Konversi DataFrame menjadi list of dictionary
data_list = df.to_dict(orient='records')

# Sisipkan seluruh data ke dalam koleksi menggunakan insert_many
result = collection.insert_many(data_list)

print(f"Data berhasil diinsert. Total {len(result.inserted_ids)} dokumen ditambahkan.")
print(f"ID dokumen yang diinsert: {result.inserted_ids}")

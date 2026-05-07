import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# module
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["sensor"]

# ambil data sensor
cursor = collection.find({}, {"_id": 0})
df = pd.DataFrame(list(cursor))

df['timestamp'] = pd.to_datetime(df['timestamp'])
# 1. Jadikan timestamp sebagai index
df.set_index('timestamp', inplace=True)


# 2. INI OBAT KUSUTNYA: Urutin index (waktu) dari lama ke baru
df.sort_index(inplace=True)

resampled = df.resample('10min').mean(numeric_only=True)
print(resampled.head())

plt.figure(figsize=(10,5))

# Plotting datanya
df['suhu'].plot(title='Suhu dari Waktu ke Waktu')

plt.ylabel('Suhu (°C)')
plt.grid(True)
plt.savefig('suhu_plot1.png')
plt.show()

resampled.to_csv('agregasi.csv')
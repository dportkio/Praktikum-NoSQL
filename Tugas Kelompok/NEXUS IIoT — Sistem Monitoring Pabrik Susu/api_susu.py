from flask import Flask, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
import csv
import io
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 948))
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_AUTH_DB = os.getenv("MONGO_AUTH_DB")
DATABASE_NAME = os.getenv("DATABASE_NAME")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource={MONGO_AUTH_DB}"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
col_monitoring = db["monitoring_susu"]


@app.route('/api/status', methods=['GET'])
def get_status():
    areas = ["Tangki Susu Utama", "Jalur Pasteurisasi", "Ruang Pendingin", "Area Filling", "Tangki Fermentasi"]
    
    pipeline = [
        {"$match": {"area": {"$in": areas}}},
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$area",
            "data_lengkap": {"$first": "$$ROOT"}
        }}
    ]

    hasil_agregasi = col_monitoring.aggregate(pipeline)
    
    data_terkini = {}
    for item in hasil_agregasi:
        area = item["_id"]
        latest = item["data_lengkap"]
        latest.pop('_id', None)
        data_terkini[area] = latest
        
    return jsonify(data_terkini)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    pipeline = [
        {"$match": {"area": "Tangki Susu Utama"}},

        {"$group": {
            "_id": "$area",
            "suhu_rata_rata": {"$avg": "$suhu"},
            "suhu_tertinggi": {"$max": "$suhu"},
            "suhu_terendah": {"$min": "$suhu"},
            "total_data_masuk": {"$sum": 1}
        }}
    ]

    hasil_agregasi = list(col_monitoring.aggregate(pipeline))
    
    if hasil_agregasi:
        data_stats = hasil_agregasi[0]
        
        if data_stats.get("suhu_rata_rata"):
            data_stats["suhu_rata_rata"] = round(data_stats["suhu_rata_rata"], 2)
            
        return jsonify(data_stats)
    else:
        return jsonify({"pesan": "Belum ada data untuk dianalisis"}), 404

if __name__ == '__main__':
    print("Menjalankan API Server di http://localhost:5000")
    app.run(port=5000, debug=True)
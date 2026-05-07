# import os
# from dotenv import load_dotenv
# from pymongo import MongoClient

# load_dotenv()
# client = MongoClient(os.getenv("MONGO_URI"))
# db = client[os.getenv("DB_NAME")]
# collection = db["sensor"]

# pipeline = [
#     {"$group": {
#         "_id": "$mesin",
#         "rata_suhu": {"$avg": "$suhu"},
#         "max_getaran": {"$max": "$getaran"},
#         "count": {"$sum": 1}
#     }},
#     {"$sort": {"rata_suhu": -1}}
# ]

# results = collection.aggregate(pipeline)
# print("Rata-rata suhu per mesin:")
# for doc in results:
#     print(f"{doc['_id']} -> rata:{doc['rata_suhu']:.2f}°C, max getaran:{doc['max_getaran']}, jumlah data:{doc['count']}")

# client.close()

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["sensor"]

pipeline = [
    {"$group": {
        "_id": "$mesin",
        "rata_suhu": {"$avg": "$suhu"},
        "max_getaran": {"$max": "$getaran"},
        "count": {"$sum": 1}
    }},
    {"$sort": {"rata_suhu": -1}}
]

results = collection.aggregate(pipeline)
print("Rata-rata suhu per mesin:")
for doc in results:
    print(f"{doc['_id']} -> rata:{doc['rata_suhu']:.2f}°C, max getaran:{doc['max_getaran']}, jumlah data:{doc['count']}")

client.close()
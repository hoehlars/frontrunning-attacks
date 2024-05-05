from datetime import datetime, date

import pymongo
from pymongo.mongo_client import MongoClient
from bson.json_util import dumps

class InsertionAtkLiveDAO():
    def __init__(self):
        uri = "mongodb+srv://larshoehener:4JYDS9UYJ5VOZvgR@cluster0.sd1cyte.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri)
        try:
            client.admin.command('ping')
            print('Successfully connected to MongoDB')
        except Exception as e:
            print(e)

        mydb = client["liveTransactionsEthDb"]
        self.live_transactions_collection = mydb["liveTransactionsClassification"]

    def get_live_transactions(self):
        latest_ten_record = self.live_transactions_collection.find().sort('_id', pymongo.DESCENDING).limit(10)

        live_transactions = []
        for record in latest_ten_record:
            date = record['time'].strftime("%d.%m.%Y")
            time = record['time'].strftime("%H:%M:%S")
            transaction = {
                'time': time,
                'date': date,
                'gasPrice': record['gasPrice'],
                'isAttack': record['is_attack'],
                'transaction_hash': str(record['transactionHash']),
                'ethAmount': record['ethAmount']
            }

            live_transactions.append(transaction)
        return live_transactions

import pymongo
from pymongo.mongo_client import MongoClient


class InsertionAtkDAO:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        client = MongoClient(mongo_uri)
        try:
            client.admin.command('ping')
            print('Successfully connected to MongoDB')
        except Exception as e:
            print(e)

        mydb = client[mongo_db]
        self.live_transactions_collection = mydb[mongo_collection]

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

    def get_atk_transactions_time_series(self):
        pipeline = [
            {
                "$match": {"is_attack": True}  # Filter documents where is_attack is true
            },
            {
                "$project": {
                    "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$time"}}
                }
            },
            {
                "$group": {
                    "_id": "$day",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]

        return list(self.live_transactions_collection.aggregate(pipeline))

    def get_last_ten_atk_transactions(self):
        latest_ten_atk_records = self.live_transactions_collection.find({"is_attack": True}).sort('_id', pymongo.DESCENDING).limit(5)

        records = []
        for record in latest_ten_atk_records:
            date = record['time'].strftime("%d.%m.%Y")
            time = record['time'].strftime("%H:%M:%S")
            transaction = {
                'time': time,
                'date': date,
                'gasPrice': record['gasPrice'],
                'transaction_hash': str(record['transactionHash']),
                'ethAmount': record['ethAmount']
            }

            records.append(transaction)
        return records



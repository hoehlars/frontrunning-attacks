from datetime import datetime
from pymongo.mongo_client import MongoClient


class LiveTransactionsDAO:
    def __init__(self, web3):
        self.web3 = web3
        uri = "mongodb+srv://larshoehener:4JYDS9UYJ5VOZvgR@cluster0.sd1cyte.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        client = MongoClient(uri)

        try:
            client.admin.command('ping')
            print('Successfully connected to MongoDB')
        except Exception as e:
            print(e)

        mydb = client["liveTransactionsEthDb"]
        self.live_transactions_collection = mydb["liveTransactionsClassification"]

    def insert_transaction(self, transaction, is_attack):
        transaction_hash = transaction['hash']
        gasPrice = transaction['gasPrice']
        insert_transaction = {'time': datetime.now(),
                              'transaction': transaction,
                              'transactionHash': transaction_hash.hex(),
                              'gasPrice': float(self.web3.from_wei(gasPrice, "gwei")),
                              'is_attack': is_attack,
                              'ethAmount': float(self.web3.from_wei(transaction['value'], 'ether'))
                              }
        try:
            self.live_transactions_collection.insert_one(insert_transaction)
        except Exception as e:
            print(e)

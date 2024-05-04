from flask import request, jsonify

from flask import Flask
from flask_cors import CORS
from web3 import Web3

from application.backend.insertion_atk_heuristics import InsertionAtkHeuristics
from application.backend.insertion_atk_live_dao import InsertionAtkLiveDAO
from application.backend.insertion_atk_model import InsertionAtkModel

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

web3 = Web3(Web3.HTTPProvider("https://intensive-sly-mountain.quiknode.pro/a3f5256d7f2af6541d483cce3f1d49c94c01879e/"))
print(web3.is_connected())
insertion_atk_model = InsertionAtkModel(web3)
insertion_atk_heuristics = InsertionAtkHeuristics()
insertion_atk_live_dao = InsertionAtkLiveDAO()


@app.route('/api/block/getInsertionAtkHeuristics/<block_number>', methods=['GET'])
def get_heuristics_result(block_number):
    print(f'blocknumber received: {block_number}')
    return jsonify({'transactions': insertion_atk_heuristics.get_transactions()})


@app.route('/api/transaction/getModelResult/<transaction_hash>', methods=['GET'])
def get_model_result(transaction_hash):
    print(f'transaction hash: {transaction_hash}')
    return jsonify({'attack': insertion_atk_model.predict()})


@app.route('/api/transaction/getLiveTransactions', methods=['GET'])
def get_live_transactions():
    return jsonify({'live_transactions': insertion_atk_live_dao.get_live_transactions()})


app.run(port=5000)

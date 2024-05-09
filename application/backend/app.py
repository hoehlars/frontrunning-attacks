from flask import request, jsonify

from flask import Flask
from flask_cors import CORS
from web3 import Web3

from application.backend.insertion_atk_heuristics import InsertionAtkHeuristics
from application.backend.insertion_atk_dao import InsertionAtkDAO

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

web3 = Web3(Web3.HTTPProvider("https://intensive-sly-mountain.quiknode.pro/a3f5256d7f2af6541d483cce3f1d49c94c01879e/"))
print(f'Connected to web3: {web3.is_connected()}')
insertion_atk_heuristics = InsertionAtkHeuristics()
insertion_atk_dao = InsertionAtkDAO()


@app.route('/api/block/getInsertionAtkHeuristics/<block_number>', methods=['GET'])
def get_heuristics_result(block_number):
    print(f'blocknumber received: {block_number}')
    return jsonify({'transactions': insertion_atk_heuristics.get_transactions()})



@app.route('/api/transaction/getLiveTransactions', methods=['GET'])
def get_live_transactions():
    return jsonify(insertion_atk_dao.get_live_transactions())

@app.route('/api/transaction/getAttackTransactionTimeSeries', methods=['GET'])
def get_atk_transaction_time_series():
    return jsonify(insertion_atk_dao.get_atk_transactions_time_series())

@app.route('/api/transaction/getLastAttackTransactions', methods=['GET'])
def get_last_ten_atk_transactions():
    return jsonify(insertion_atk_dao.get_last_ten_atk_transactions())


app.run(port=5000)

from flask import jsonify

from flask import Flask
from flask_cors import CORS
from web3 import Web3

from insertion_atk_heuristics import InsertionAtkHeuristics
from insertion_atk_dao import InsertionAtkDAO
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

node_url = os.getenv("NODE_URL")
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")
mongo_collection = os.getenv("MONGO_COLLECTION")
etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")
web3 = Web3(Web3.HTTPProvider(node_url))

print(f'Connected to web3: {web3.is_connected()}')
insertion_atk_heuristics = InsertionAtkHeuristics(web3, etherscan_api_key)
insertion_atk_dao = InsertionAtkDAO(mongo_uri, mongo_db, mongo_collection)


@app.route('/api/block/getInsertionAtkHeuristics/<block_number>', methods=['GET'])
def get_heuristics_result(block_number):
    print(f'blocknumber received: {block_number}')
    return jsonify(insertion_atk_heuristics.get_transactions_by_block_number(block_number))


@app.route('/api/block/getInsertionAtkHeuristics/<int:block_number_from>/<int:block_number_to>', methods=['GET'])
def get_heuristics_cost_profit(block_number_from, block_number_to):
    print(f'Block-range received: {block_number_from}, {block_number_to}')
    return insertion_atk_heuristics.get_cost_profit_by_block_range(block_number_from, block_number_to).to_json(orient='records')

@app.route('/api/transaction/getModelAndHeuristicsClassification/<transaction_hash>', methods=['GET'])
def get_classifiaction_by_model_and_heuristics(transaction_hash):
    print(f'Transaction Hash received: {transaction_hash}')
    return jsonify(insertion_atk_heuristics.check_transaction_classified_by_model_and_heuristics(transaction_hash))

@app.route('/api/transaction/getLiveTransactions', methods=['GET'])
def get_live_transactions():
    return jsonify(insertion_atk_dao.get_live_transactions())


@app.route('/api/transaction/getAttackTransactionTimeSeries', methods=['GET'])
def get_atk_transaction_time_series():
    return jsonify(insertion_atk_dao.get_atk_transactions_time_series())


@app.route('/api/transaction/getLastAttackTransactions', methods=['GET'])
def get_last_ten_atk_transactions():
    return jsonify(insertion_atk_dao.get_last_ten_atk_transactions())

app.run(debug=True, host='0.0.0.0', port=5000)

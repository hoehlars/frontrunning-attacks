import pandas as pd
from heuristics.InsertionAttackHeuristicsDetector import InsertionAttackHeuristicsDetector
from model.FeaturePreparer import FeaturePreparer
from model.network import Network


class InsertionAtkHeuristics:
    def __init__(self, web3, etherscan_api_key):
        self.web3 = web3
        self.insertionAttackDetector = InsertionAttackHeuristicsDetector(web3)
        self.network = Network()
        self.feature_preparer = FeaturePreparer(web3, etherscan_api_key)

    def get_transactions_by_block_number(self, block_number):

        attacks = self.insertionAttackDetector.get_frontrunning_attacks_of_block(block_number).to_dict("records")

        records = []

        for attack in attacks:
            record = {
                'transactions': {
                    'attack1': {
                        'address': attack["first_attacker"],
                        'hash': attack["tx_hash_first_attacker"],
                        'gasFees': attack["gas_fees_first_attacker"],
                        'amount': attack["usd_spent_first_attacker"]
                    },
                    'victim': {
                        'address': attack["victim"],
                        'hash': attack["tx_hash_victim"],
                        'gasFees': attack["gas_fees_victim"],
                        'amount': attack["usd_spent_victim"]
                    },
                    'attack2': {
                        'address': attack["second_attacker"],
                        'hash': attack["tx_hash_second_attacker"],
                        'gasFees': attack["gas_fees_second_attacker"],
                        'amount': attack["usd_spent_second_attacker"]
                    }
                },
                'attackInformation':
                    {
                        'cost': attack["cost"],
                        'profit': attack["profit"],
                        'tokenName': attack["token_name"],
                        'tokenAddress': attack["token_contract_address"]
                    }
            }

            records.append(record)

        return records

    def get_cost_profit_by_block_range(self, block_number_from, block_number_to):

        block_range = list(range(block_number_from, block_number_to + 1))

        df_attacks_in_block_range = pd.DataFrame()

        for block_number in block_range:
            try:
                df_attacks = self.insertionAttackDetector.get_frontrunning_attacks_of_block(block_number)
                df_attacks_in_block_range = pd.concat([df_attacks_in_block_range, df_attacks], ignore_index=True)
            except:
                continue

        if df_attacks_in_block_range.empty:
            return df_attacks_in_block_range

        return df_attacks_in_block_range.groupby('blockNumber').sum().reset_index()[["blockNumber", "profit", "cost"]]

    def check_transaction_classified_by_model_and_heuristics(self, transaction_hash):
        classified_by_model = False
        classified_by_heuristics = False

        try:
            transaction = self.web3.eth.get_transaction(transaction_hash)
        except:
            return None

        if not transaction:
            return {"transactionHash": transaction_hash, "isModelAttack": classified_by_model,
                    "isHeuristicsAttack": classified_by_heuristics}

        block_number = transaction["blockNumber"]

        # Check if classified by heuristics
        classified_by_heuristics = self.check_transaction_classified_by_heuristics(block_number,
                                                                                   transaction_hash)

        # Check if classified by model
        model_features = self.create_model_features(transaction_hash, transaction, block_number)
        classified_by_model = self.check_transaction_classified_by_model(model_features)

        return {"transactionHash": transaction_hash,
                "isModelAttack": classified_by_model,
                "isHeuristicsAttack": classified_by_heuristics,
                "blockNumber": block_number,
                "modelFeatures": {
                    "gasPrice": int(model_features[0] * 100) / 100,
                    "meanGasPriceLast10Blocks": round(model_features[1], 2),
                    "stdGasPriceLast10Blocks": round(model_features[2], 2),
                    "meanGasPriceLast10BlocksSameEAO": round(model_features[3], 2),
                    "stdGasPriceLast10BlocksSameEAO": round(model_features[4], 2),
                    "usedGasToken": model_features[5],
                    "predictedGasPrice": round(model_features[6], 2)
                }
        }

    def check_transaction_classified_by_heuristics(self, block_number, transaction_hash):
        classified_by_heuristics = False

        df_attacks = self.insertionAttackDetector.get_frontrunning_attacks_of_block(block_number)

        if not df_attacks.empty:
            if transaction_hash in df_attacks["tx_hash_first_attacker"].unique() or transaction_hash in df_attacks[
                "tx_hash_second_attacker"].unique():
                classified_by_heuristics = True

        return classified_by_heuristics

    def check_transaction_classified_by_model(self, features):

        is_attack = self.network.get_prediction(features)
        return is_attack

    def create_model_features(self, transaction_hash, transaction, block_number):
        gas_price = self.feature_preparer.convert_from_wei_to_gwei(transaction["gasPrice"])

        self.feature_preparer.get_mean_and_std_gas_price_of_last_n_blocks(10, block_number)
        address = transaction["from"]

        self.feature_preparer.get_mean_and_std_gas_price_of_last_n_blocks_of_same_EOA(10, block_number, address)
        last_15_gas_prices = self.feature_preparer.get_last_15_gas_prices(transaction_hash)

        predicted_gas_price = self.feature_preparer.get_predicted_gas_price(last_15_gas_prices)
        used_gas_token = self.feature_preparer.is_gas_token_contract_in_internal_transaction(transaction['hash'])

        features = [gas_price,
                    self.feature_preparer.mean_gas_price_last_10_blocks,
                    self.feature_preparer.std_price_last_10_blocks,
                    self.feature_preparer.mean_gas_price_last_10_blocks_same_EOA,
                    self.feature_preparer.std_gas_price_last_10_blocks_same_EOA,
                    used_gas_token,
                    predicted_gas_price]

        return features

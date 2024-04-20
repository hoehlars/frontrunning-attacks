import numpy as np
import torch
import requests

import requests

class FeaturePreparer:
    def __init__(self, web3):
        self.web3 = web3
        self.curr_block = 0
        self.mean_gas_price_last_10_blocks = 0
        self.std_price_last_10_blocks = 0
        self.mean_gas_price_last_10_blocks_same_EOA = 0
        self.std_gas_price_last_10_blocks_same_EOA = 0
        self.last_15_transactions_cache = []
        self.transaction_count = 0
        self.processed_transaction_count = 0

        self.model_feature_7 = torch.jit.load('../training/lstm-feature-7.pt')
        self.mean_feature_7 = torch.load('../training/mean_train.pt')
        self.std_feature_7 = torch.load('../training/std_train.pt')

    def prepare(self, transaction, curr_block):
        self.add_transaction_to_cache(transaction)

        print(transaction["gasPrice"])

        if len(self.last_15_transactions_cache) < 15:
            return

        gas_price = transaction["gasPrice"]

        if self.curr_block != curr_block:
            self.curr_block = curr_block
            self.get_mean_and_std_gas_price_of_last_n_blocks(
                10, curr_block)
        address = transaction["from"]
        self.get_mean_and_std_gas_price_of_last_n_blocks_of_same_EOA(
                10, curr_block, address)

        predicted_gas_price = self.get_predicted_gas_price()

        return (gas_price, self.mean_gas_price_last_10_blocks, self.std_price_last_10_blocks,
                self.mean_gas_price_last_10_blocks_same_EOA,
                self.std_gas_price_last_10_blocks_same_EOA, predicted_gas_price)


    def get_mean_and_std_gas_price_of_last_n_blocks(self, last_n_blocks, curr_block):
        gas_prices = []
        for i in range(last_n_blocks):
            block = self.web3.eth.get_block(curr_block - i, full_transactions=True)

            for transaction in block.transactions:
                gas_prices.append(transaction["gasPrice"])

        self.mean_gas_price_last_10_blocks = np.mean(gas_prices)
        self.std_price_last_10_blocks = np.std(gas_prices)

    def get_mean_and_std_gas_price_of_last_n_blocks_of_same_EOA(self, last_n_blocks, curr_block, eoa_address):
        gas_prices = []
        for i in range(last_n_blocks):
            block = self.web3.eth.get_block(curr_block - i, full_transactions=True)

            for transaction in block.transactions:
                if transaction["from"] == eoa_address:
                    gas_prices.append((transaction["gasPrice"]))

        if len(gas_prices) == 0:
            self.mean_gas_price_last_10_blocks_same_EOA = 0
            self.std_gas_price_last_10_blocks_same_EOA = 0
        else:
            self.mean_gas_price_last_10_blocks_same_EOA = np.mean(gas_prices)
            self.std_gas_price_last_10_blocks_same_EOA = np.std(gas_prices)

    def add_transaction_to_cache(self, transaction):
        if len(self.last_15_transactions_cache) < 15:
            self.last_15_transactions_cache.append(transaction["gasPrice"])
        else:
            index = self.transaction_count % 15
            self.last_15_transactions_cache[index] = transaction["gasPrice"]
        self.transaction_count += 1

    def get_predicted_gas_price(self):
        self.model_feature_7.eval()
        '''
        with torch.no_grad():
            tensor = torch.tensor(self.last_15_transactions_cache).view(1, 1, 15)
            predicted_curr_gas_price = self.model_feature_7(tensor)[:, -1].item()
            return predicted_curr_gas_price * self.std_feature_7.item() + self.mean_feature_7.item()
        '''

    def is_gas_token_contract_in_internal_transaction(self, transaction_hash):

        gas_token_addresses = {"0x0000000000b3f879cb30fe243b4dfee438691c04": "GST2",
                               "0x88d60255f917e3eb94eae199d827dad837fac4cb": "GST1",
                               "0x0000000000004946c0e9f43f4dee607b0ef1fa1c": "CHI"}

        internal_transactions = get_internal_transactions(transaction_hash)

        if not internal_transactions:
            return False

        for transaction in internal_transactions:
            if transaction["from"] in gas_token_addresses.keys():
                # print(f"'{gas_token_addresses[transaction['from']]}' is used in {transaction['type']}")
                return True
            if transaction["to"] in gas_token_addresses.keys():
                # print(f"'{gas_token_addresses[transaction['to']]}' is used in {transaction['type']}")
                return True

        return False

    def get_internal_transactions(self, tx_hash):
        # API endpoint
        url = 'https://api.etherscan.io/api'

        # Parameters
        params = {
            'module': 'account',
            'action': 'txlistinternal',
            'txhash': tx_hash,
            'apikey': '1PN1111XBM2W5HIQCSMQH6RA65JVYPQM1R'
        }

        try:
            # Sending GET request
            response = requests.get(url, params=params, timeout=3)

            # Checking if request was successful
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                # print('Error occurred:', response.status_code)
                return None

        except requests.exceptions.Timeout:
            # print('Request did not go through: timeout occurred')
            return None
import numpy as np
import torch

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

        self.model_feature_7 = torch.jit.load('./lstm-feature-7.pt')
        self.mean_feature_7 = torch.load('./mean_train.pt')
        self.std_feature_7 = torch.load('./std_train.pt')

    def prepare(self, transaction, curr_block):
        self.add_transaction_to_cache(transaction)

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
        with torch.no_grad():
            tensor = torch.tensor(self.last_15_transactions_cache).view(1, 1, 15)
            predicted_curr_gas_price = self.model_feature_7(tensor)[:, -1].item()
            return predicted_curr_gas_price * self.std_feature_7.item() + self.mean_feature_7.item()
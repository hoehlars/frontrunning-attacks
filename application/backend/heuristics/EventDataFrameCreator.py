import pandas as pd


class EventDataFrameCreator:

    def __init__(self, web3):
        self.web3 = web3

    def get_checksum_address_from_topics_hash(self, topics_hash):
        return self.web3.to_checksum_address(topics_hash.hex().replace("0x", "")[24:64])

    def get_amount_of_tokens_from_data_hash(self, data_hash):
        return int(data_hash.hex().replace("0x", "")[0:64], 16)

    def create_df_of_events(self, events_by_address):

        df = pd.DataFrame(columns=['contractAddress',
                                   'transactionIndex',
                                   'logIndex',
                                   'transactionHash',
                                   'wallet',
                                   'sender',
                                   'receiver',
                                   'gasPrice',
                                   'amount'])

        for token_contract_address in events_by_address:

            nr_of_transactions_with_same_coin = len(events_by_address[token_contract_address])

            # At least 3 transactions (A1, V, A2)
            if nr_of_transactions_with_same_coin <= 2:
                continue

            for transaction in events_by_address[token_contract_address]:
                transaction_hash = transaction["transactionHash"].hex()
                tx_by_hash = self.web3.eth.get_transaction(transaction_hash)

                if len(transaction["topics"]) <= 1:
                    break

                record = {
                    "contractAddress": token_contract_address,
                    "transactionIndex": transaction["transactionIndex"],
                    "logIndex": transaction["logIndex"],
                    "transactionHash": transaction_hash,
                    "wallet": tx_by_hash["from"],
                    "sender": self.get_checksum_address_from_topics_hash(transaction["topics"][1]),
                    "receiver": self.get_checksum_address_from_topics_hash(transaction["topics"][2]),
                    "gasPrice": tx_by_hash["gasPrice"] / 10 ** 9,
                    "amount": self.get_amount_of_tokens_from_data_hash(transaction["data"])
                }
                new_df = pd.DataFrame([record])
                df = pd.concat([df, new_df], ignore_index=True)

        return df

    def create_df_grouped_by_transaction_index(self, df_of_events):

        df_final = pd.DataFrame(columns=['contractAddress',
                                         'transactionIndex',
                                         'transactionHash',
                                         'wallet',
                                         'first_sender',
                                         'first_receiver',
                                         'last_sender',
                                         'last_receiver',
                                         'gasPrice',
                                         'amount'])

        unique_token_contract_addresses = df_of_events["contractAddress"].unique()

        df_grouped_by_contractAddress_and_transactionIndex = \
        df_of_events.groupby(['contractAddress', 'transactionIndex'])['logIndex'].agg(['min', 'max']).reset_index()

        for token_contract_address in unique_token_contract_addresses:

            df_grouped_subset = df_grouped_by_contractAddress_and_transactionIndex[
                df_grouped_by_contractAddress_and_transactionIndex["contractAddress"] == token_contract_address]

            for index, row in df_grouped_subset.iterrows():
                transaction_index = row["transactionIndex"]
                min_log_index = row["min"]
                max_log_index = row["max"]

                min_log_index_row = df_of_events[
                    (df_of_events["contractAddress"] == token_contract_address) &
                    (df_of_events["transactionIndex"] == transaction_index) &
                    (df_of_events["logIndex"] == min_log_index)
                    ]

                first_sender = min_log_index_row.iloc[0]["sender"]
                first_receiver = min_log_index_row.iloc[0]["receiver"]

                transaction_hash = min_log_index_row.iloc[0]["transactionHash"]
                wallet = min_log_index_row.iloc[0]["wallet"]
                gasPrice = min_log_index_row.iloc[0]["gasPrice"]
                amount = min_log_index_row.iloc[0]["amount"]

                max_log_index_row = df_of_events[
                    (df_of_events["contractAddress"] == token_contract_address) &
                    (df_of_events["transactionIndex"] == transaction_index) &
                    (df_of_events["logIndex"] == max_log_index)
                    ]

                last_sender = max_log_index_row.iloc[0]["sender"]
                last_receiver = max_log_index_row.iloc[0]["receiver"]

                record = {
                    "contractAddress": token_contract_address,
                    "transactionIndex": transaction_index,
                    "transactionHash": transaction_hash,
                    "wallet": wallet,
                    "first_sender": first_sender,
                    "first_receiver": first_receiver,
                    "last_sender": last_sender,
                    "last_receiver": last_receiver,
                    "gasPrice": gasPrice,
                    "amount": amount
                }

                new_df = pd.DataFrame([record])
                df_final = pd.concat([df_final, new_df], ignore_index=True)

        return df_final
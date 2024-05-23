import pandas as pd
from application.backend.heuristics.EventDataFrameCreator import EventDataFrameCreator
from application.backend.heuristics.CostProfitCalculator import CostProfitCalculator


class InsertionAttackHeuristicsDetector:

    TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"  # ERC20 "Transfer"

    def __init__(self, web3):
        self.web3 = web3
        self.event_df_creator = EventDataFrameCreator(web3)
        self.cost_profit_calculator = CostProfitCalculator(web3)
        pass

    def search_attacks_for_block_range(self, from_block, to_block):
        pass

    def get_events_by_contract_address(self, events):

        events_by_address = {}

        for event in events:

            token_contract_address = event["address"]

            if token_contract_address in events_by_address:
                events_by_address[token_contract_address].append(event)
            else:
                events_by_address[token_contract_address] = [event]

        return events_by_address

    def get_rows_with_similar_amounts(self, df):

        def is_similar(value1, value2):
            # Check if the absolute difference between the values is within 1% of the larger value
            diff_percentage = abs(value1 - value2) / max(value1, value2) * 100
            return diff_percentage <= 1

        rows_with_similar_amount = []

        column_name = "amount"

        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                value1 = df.at[i, column_name]
                value2 = df.at[j, column_name]
                if is_similar(value1, value2):
                    rows_with_similar_amount.append((i, j))

        return rows_with_similar_amount

    def find_victim_transactions(self, atk1_idx, atk2_idx, df):

        atk1_sender = df.iloc[atk1_idx]["first_sender"]
        possible_victims_df = df.iloc[atk1_idx + 1:atk2_idx].sort_values(by="transactionIndex", ascending=False)

        for i in range(len(possible_victims_df)):

            victim_transaction = possible_victims_df.iloc[i]
            victim_receiver = victim_transaction["first_sender"]

            # Heuristic 1 (part of it)
            if not atk1_sender == victim_receiver:
                continue

            return victim_transaction

        return None

    def get_token_name_from_contract_address(self, contract_address):

        try:
            token_contract = self.web3.eth.contract(address=contract_address, abi=[
                {"constant": True, "inputs": [], "name": "name",
                 "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False,
                 "stateMutability": "view", "type": "function"}])
            return token_contract.functions.name().call()
        except:
            return None

    def get_attacks_for_contract_address(self, df, contract_address, block_nr):

        attack_df_by_transaction_index = pd.DataFrame()

        # Heuristics 3 already grouped by contract address
        # Heuristics 5 (sorting by transaction index)
        df_contract_address = df[df["contractAddress"] == contract_address].sort_values(
            by="transactionIndex").reset_index(drop=True)

        # Heuristics 2
        rows_with_similar_amount = self.get_rows_with_similar_amounts(df_contract_address)

        for combination in rows_with_similar_amount:

            row1_idx = combination[0]
            row2_idx = combination[1]

            if row2_idx - row1_idx <= 1:
                continue

            row1 = df_contract_address.iloc[row1_idx]
            row2 = df_contract_address.iloc[row2_idx]

            # Heuristic 1 (part of it)
            if not row1["first_sender"] == row2["last_receiver"]:
                continue

            if not row1["first_receiver"] == row2["last_sender"]:
                continue

            # Heuristics 6
            if not row1["gasPrice"] > row2["gasPrice"]:
                continue

            victim_transaction = self.find_victim_transactions(row1_idx, row2_idx, df_contract_address)

            if victim_transaction is None:
                continue

            # Heuristics 4
            if not row1["transactionHash"] != victim_transaction["transactionHash"] and row2["transactionHash"] != \
                    victim_transaction["transactionHash"]:
                continue

            try:
                profit, cost, usd_spent = self.cost_profit_calculator.calculate_cost_and_profit_in_usd(block_nr,
                                                                                                       row1["transactionHash"],
                                                                                                       row2["transactionHash"],
                                                                                                       victim_transaction["transactionHash"])
            except:
                print("Could not calculate USD price")
                profit, cost, usd_spent = 0, 0, [0, 0, 0]


            attack_record = {
                "blockNumber": block_nr,
                "first_attacker": row1["wallet"],
                "victim": victim_transaction["wallet"],
                "second_attacker": row2["wallet"],
                "tx_hash_first_attacker": row1["transactionHash"],
                "tx_hash_victim": victim_transaction["transactionHash"],
                "tx_hash_second_attacker": row2["transactionHash"],
                "first_victim_gas_price_delta": round(row1["gasPrice"] - victim_transaction["gasPrice"], 2),
                "gas_fees_first_attacker": int(row1["gasPrice"] * 100) / 100,
                "gas_fees_victim": int(victim_transaction["gasPrice"] * 100) / 100,
                "gas_fees_second_attacker": int(row2["gasPrice"] * 100) / 100,
                "victim_second_gas_price_delta": round(victim_transaction["gasPrice"] - row2["gasPrice"], 2),
                "profit": round(profit,2),
                "cost": round(cost,2),
                "usd_spent_first_attacker": round(usd_spent[0],2),
                "usd_spent_victim": round(usd_spent[1], 2),
                "usd_spent_second_attacker": round(usd_spent[2], 2),
                "token_contract_address": contract_address,
                "token_name": self.get_token_name_from_contract_address(contract_address),
            }

            new_df = pd.DataFrame([attack_record])
            attack_df_by_transaction_index = pd.concat([attack_df_by_transaction_index, new_df], ignore_index=True)

        return attack_df_by_transaction_index

    def get_frontrunning_attacks_of_block(self, block_nr):

        TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

        block_nr = int(block_nr)
        print(block_nr)

        events = self.web3.eth.filter({"fromBlock": block_nr, "toBlock": block_nr, "topics": [TRANSFER]}).get_all_entries()

        events_by_address = self.get_events_by_contract_address(events)

        df_of_events = self.event_df_creator.create_df_of_events(events_by_address)
        df_grouped_by_transaction_index = self.event_df_creator.create_df_grouped_by_transaction_index(df_of_events)

        unique_token_contract_addresses = df_grouped_by_transaction_index["contractAddress"].unique()

        df_attacks_in_block = pd.DataFrame()

        for token_contract_address in unique_token_contract_addresses:
            df_attacks = self.get_attacks_for_contract_address(df_grouped_by_transaction_index, token_contract_address,
                                                          block_nr)
            df_attacks_in_block = pd.concat([df_attacks_in_block, df_attacks], ignore_index=True)

        # Some transactions involve event-chain, which are recognized as attacks multiple times. Just keep once by removing duplicates
        df_attacks_in_block.drop_duplicates(subset=['blockNumber', 'first_attacker', 'victim', 'second_attacker'],
                                            keep='last', inplace=True)

        return df_attacks_in_block
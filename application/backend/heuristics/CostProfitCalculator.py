import requests


class CostProfitCalculator:

    def __init__(self, web3):
        self.web3 = web3

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
                return data["result"]
            else:
                # print('Error occurred:', response.status_code)
                return None

        except requests.exceptions.Timeout:
            # print('Request did not go through: timeout occurred')
            return None

    def get_eth_rate_at_time(self, timestamp):
        # CryptoCompare API endpoint for historical Ethereum price
        url = f"https://min-api.cryptocompare.com/data/pricehistorical?fsym=ETH&tsyms=USD&ts={timestamp}&extraParams=your_app_name"

        # Send GET request to CryptoCompare API
        response = requests.get(url)

        # Parse JSON response
        data = response.json()

        # Check if response contains data
        if 'ETH' in data and 'USD' in data['ETH']:
            eth_price_usd = data['ETH']['USD']
            return eth_price_usd
        else:
            return None

    def get_block_timestamp(self, block_number):
        block = self.web3.eth.get_block(block_number)
        timestamp = block['timestamp']
        return timestamp

    def get_amount_eth_spent(self, transaction_hash):
        internal_transaction = self.get_internal_transactions(transaction_hash)
        amount_in_wei = int(internal_transaction[0]["value"])
        return amount_in_wei / 10 ** 18

    def get_amount_gas_spent(self, transaction_hash):
        transaction = self.web3.eth.get_transaction_receipt(transaction_hash)
        gas_used = transaction["gasUsed"]
        gas_price = transaction["effectiveGasPrice"] / 10 ** 18

        return gas_used * gas_price

    def calculate_cost_and_profit_in_usd(self, block_nr, attack_tx_1, attack_tx_2, victim_tx):
        # Get amount in ETH, which were spent to buy same coins as victim
        eth_spent = self.get_amount_eth_spent(attack_tx_1)
        # Get gas fees from attack 1 and attack 2 transaction
        eth_fees = self.get_amount_gas_spent(attack_tx_1) + self.get_amount_gas_spent(attack_tx_2)

        # Get total amount that attacker spent in attack 1 and attack 2 (for coins + fees)
        cost_eth = eth_spent + eth_fees

        # Get amount in ETH, which were received in attack 2 (when attacker sells coins again after victim bought)
        eth_received = self.get_amount_eth_spent(attack_tx_2)

        # Calculate difference of received amount minus expenses: Profit
        profit_eth = eth_received - cost_eth

        # Convert calculated values from ETH to USD using timestamp when block of attack transactions was executed
        timestamp = self.get_block_timestamp(block_nr)
        eth_rate_at_timestamp = self.get_eth_rate_at_time(timestamp)

        cost_usd_at_timestamp = eth_fees * eth_rate_at_timestamp

        profit_usd_at_timestamp = profit_eth * eth_rate_at_timestamp

        #Calculate Amount Spent in USD
        eth_spent_victim = self.get_amount_eth_spent(victim_tx)

        usd_spent_atk1 = eth_spent * eth_rate_at_timestamp
        usd_spent_atk2 = eth_received * eth_rate_at_timestamp
        usd_spent_victim = eth_spent_victim * eth_rate_at_timestamp

        return profit_usd_at_timestamp, cost_usd_at_timestamp, [usd_spent_atk1, usd_spent_victim, usd_spent_atk2]

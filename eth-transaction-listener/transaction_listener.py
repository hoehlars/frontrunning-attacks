import numpy as np
from web3 import Web3
import asyncio
from FeaturePreparer import FeaturePreparer

web3 = Web3(Web3.HTTPProvider("https://intensive-sly-mountain.quiknode.pro/a3f5256d7f2af6541d483cce3f1d49c94c01879e"))


# test to see if you are connected to your node
# this will print out True if you are successfully connected to a node
print(web3.is_connected())

feature_preparer = FeaturePreparer(web3)

def handle_event(event):
    # print the transaction hash
    # print(Web3.toJSON(event))

    # use a try / except to have the program continue if there is a bad transaction in the list
    try:
        # remove the quotes in the transaction hash
        transaction = Web3.to_json(event).strip('"')
        # use the transaction hash that we removed the '"' from to get the details of the transaction
        transaction = web3.eth.get_transaction(transaction)
        feature_preparer.prepare(transaction, web3.eth.block_number)

    except Exception as err:
        pass

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)


def main():
    # filter for pending transactions
    tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(tx_filter, 5)))
    finally:
        loop.close()

if __name__ == '__main__':
    main()
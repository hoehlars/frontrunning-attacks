# Detecting front-running attacks on Ethereum mainnet

Front-running attacks is a type of malicious behaviour, where the attacker continuously 
monitors the Ethereum transaction pool (mempool) and try to frontrun their victims 
transactions for a personal gain of money. There exist different types of front-running attacks,
in this project we focused on **insertion attacks**.  
Insertion attacks or sandwich attacks often wait for a larger transaction (also called a victim transaction). After
spotting such a victim transaction, the attacker inserts two attack transaction. The first attack transaction has a
higher gas price than the victim transaction and often is a buy transaction. The second one has a lower gas price
than the victim transaction and is a sell transaction. As the pending transactions of the Ethereum mainnet are
sorted by gas price, the order of processing is the following: first attack, victim transaction, second attack. As
the victim transaction often changes the price of the traded currency, the insertion attack can abuse arbitrage with first
buying and later on selling more expensive

## Description

To detect such insertion attacks 2 different approaches where implemented:
- A **neural network** (Multi-layer Perceptron) used for binary classification of attack & non-attack transactions
- A **heuristics algorithm** that can detect insertion attacks by heuristics

The result of the neural network model and heuristics algorithm are visualized in an interactive dashboard.


## Setup Instructions

### 1. Set up access to Ethereum mainnet

We use QuickNode for access to the Web3 API. Ensure you have a QuickNode account and obtain your endpoint URL.

### 2. Set up Mongo DB

Create a MongoDB database and a collection that will be used for storing data.

### 3. Clone Repository

```
git clone https://github.com/hoehlars/frontrunning-attacks
cd frontrunning-attacks
```

### 4. Configure Environment Variables

Rename the .env.example file to .env and insert your configuration details.

```
mv .env.example .env
```

Edit the `.env` file and add your QuickNode URL, MongoDB information, and Ethereum API key.

```
NODE_URL=<url_to_quicknode>
NODE_URL_2=<url_to_another_quicknode>
MONGO_URI=<your_mongo_uri>
MONGO_DB=<your_mongo_db>
MONGO_COLLECTION=<your_mongo_collection>
ETHERSCAN_API_KEY=<your_api_key>
```

## Executing program

### Start the services

Use Docker Compose to start the three services (frontend, backend, live-transaction-listener)

```
docker compose up [-d]
```

### Stopping the services

```
docker compose down
```

## Illustrations

### Live classification dashboard 

1. Live transactions: Classified transactions are fetched from the MongoDB in real time and visualized in
a table (top in Figure).

2. Line chart of attacks over time: The amount of all insertion attacks classified by the model are
accumulated per day and visualized as a line chart (bottom left in Figure).

3. Last 5 classified attacks:  The last 5 transactions that the model has classified as insertion attacks are
fetched from the MongoDB and visualized in a table (bottom right in Figure 3).

### Heuristics dashboard

1. Attacks by block number: Given any block number the heuristics algorithm checks if any insertion attack
can be found in that block in real time. If attacks are found, they are visualized including information about the
attackers and victims addresses, transaction hash, gas fees spent, cost, profit and the token (top in Figure).

2. Bar chart of cost and Profit by block range: Given a block range the heuristics algorithm iterates through
all block numbers and calculates the total cost and profit per block. The cost and profit are then visualized per
block as a bar chart on the dashboard (bottom left in Figure).

3. Comparison of model & heuristics by transaction hash: To compare the classification of the model and
the heuristics algorithm, a transaction hash can be searched to predict whether a transaction is an attack. The
model predicts if the transaction is an attack, while the algorithm checks if the transaction is part of an insertion
attack. The classifications of the model and the heuristics algorithm are then visualized on the dashboard as well
as a table of the features used by to the model (bottom right in Figure).

## Authors

- Lars Hoehener (github: hoehlars)
- Nico Zala (github: nczala)

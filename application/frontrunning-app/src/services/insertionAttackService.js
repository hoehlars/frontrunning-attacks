
const url = 'http://localhost:5000'

export async function getAttackTransactionFromBlock(blockNumber) {
    try {
        const response = await fetch(url + '/api/block/getInsertionAtkHeuristics/' + blockNumber, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        return await response.json();
    } catch (error) {
        console.error("Error:", error);
    }
}

export async function getCostProfitFromBlockRange(blockNumberFrom, blockNumberTo) {
    try {
        const response = await fetch(url + `/api/block/getInsertionAtkHeuristics/${blockNumberFrom}/${blockNumberTo}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        return await response.json();
    } catch (error) {
        console.error("Error:", error);
    }
}

export async function getClassificationByModelAndHeuristics(transactionHash) {
    try {
    const response = await fetch(url + '/api/transaction/getModelAndHeuristicsClassification/' + transactionHash, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            }
        });
        return await response.json();
    } catch (error) {
        console.error("Error:", error);
    }
}

export async function getLiveTransactionClassificationOfInsertionAtk() {
    try {
        const response = await fetch(url + '/api/transaction/getLiveTransactions', {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        return await response.json();
    } catch (error) {
        console.error("Error:", error);
    }
}

export async function getInsertionAtkTimeSeries() {
    try {
        const response = await fetch(url + '/api/transaction/getAttackTransactionTimeSeries', {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        return await response.json();
    } catch (error) {
        console.error("Error:", error);
    }
}

export async function getInsertionAtkTable() {
    try {
        const response = await fetch(url + '/api/transaction/getLastAttackTransactions', {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        return await response.json();
    } catch (error) {
        console.error("Error:", error);
    }
}
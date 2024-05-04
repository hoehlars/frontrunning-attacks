
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

export async function getClassificationOfInsertionAttackModel(transactionHash) {
    try {
        const response = await fetch(url + '/api/transaction/getModelResult/' + transactionHash, {
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
import styles from "./InsertionAttacksHeuristics.module.css"
import {useState} from "react";
import {
    getAttackTransactionFromBlock
} from "../../services/insertionAttackService";
import {Button, Col, InputGroup, Row, Spinner, Table} from "react-bootstrap";
import {Tooltip} from "react-tooltip";
import Form from "react-bootstrap/Form";

const transactions = [{
    "type": 'Attack',
    "gasPrice": 100,
    "ethTransfered": 50,
    "profit": 10
},
    {   "type": "Victim",
        "gasPrice": 100,
        "ethTransfered": 50,
        "profit": 10
    },
    {
        "type": "Attack",
        "gasPrice": 100,
        "ethTransfered": 50,
        "profit": 10
    }]

function InsertionAttackHeuristics() {
    const [blockNumber, setBlockNumber] = useState('');
    const [isSearching, setSearching] = useState(false);
    const [heuristicsResult, setHeuristicsResult] = useState(null);

    async function startSearching() {
        setSearching(true);
        setHeuristicsResult(null);
        const response = await getAttackTransactionFromBlock(blockNumber);
        setSearching(false);

        const resultTransactions = response.transactions
        console.log(resultTransactions)

        if(resultTransactions.length > 0) {
            setHeuristicsResult(transactions)
        }
        else {
            setHeuristicsResult([])
        }
    }

    function createTableRow(transaction, i) {
        const classType = transaction.type === 'Attack' ? 'table-danger' : 'table-success'
        return (
            <tr key={i} className={classType}>
                <td>{transaction.type}</td>
                <td>{transaction.gasPrice}</td>
                <td>{transaction.ethTransfered}</td>
                <td>{transaction.profit}</td>
            </tr>
        );
    }

    return (
        <Col className="align-content-center">
            <Row>
                <Tooltip id="tooltip-transaction-search"/>
                <InputGroup data-tooltip-id="tooltip-transaction-search" data-tooltip-content="Insert a block number here.
            As a result our heuristics will search the block for any insertion attacks."
                            className={[styles.searchBar, "mb-2"].join(" ")}>
                    <Form.Control
                        placeholder="Insert a blocknumber here"
                        aria-label="Block number"
                        aria-describedby="basic-addon2"
                        onChange={e => setBlockNumber(e.target.value)}
                    />
                    <Button variant="primary" id="button-addon2" onClick={startSearching}>
                        Search
                    </Button>
                </InputGroup>
                <Tooltip text="123"></Tooltip>
            </Row>
            <Row className={["justify-content-center", styles.searchResult].join(" ")}>
                {isSearching ? <Spinner animation="border" variant="primary"/> : null}
                {heuristicsResult && heuristicsResult.length > 0 ?
                    <Table className={styles.resultTable}>
                        <thead className="table-dark">
                        <tr>
                            <th>Type</th>
                            <th>Gas Price</th>
                            <th>ETH Transfered</th>
                            <th>Profit</th>
                        </tr>
                        </thead>
                        <tbody>
                        {heuristicsResult.map((transaction, i) => createTableRow(transaction, i))}
                        </tbody>
                    </Table>: null}
                {heuristicsResult && heuristicsResult.length === 0 ?
                    <p>There were no insertion attack found in {blockNumber}</p> : null}
            </Row>
        </Col>);
}

export default InsertionAttackHeuristics;
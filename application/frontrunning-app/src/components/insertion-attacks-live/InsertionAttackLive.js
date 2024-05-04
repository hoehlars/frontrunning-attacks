import styles from "./InsertionAttackLive.module.css"
import {useEffect, useState} from "react";
import {getLiveTransactionClassificationOfInsertionAtk} from "../../services/insertionAttackService";
import {Col, Row, Spinner, Table} from "react-bootstrap";
function InsertionAttackLive() {
    const [liveTransactions, setLiveTransactions] = useState(null);
    const POLLING_INTERVAL = 5000;

    useEffect(() => {
        const intervalId = setInterval(async () => {
            const response = await getLiveTransactionClassificationOfInsertionAtk();
            const result = response['live_transactions']
            const sortedResult = result.sort((a, b) => a.index > b.index)
            setLiveTransactions(sortedResult);
        }, POLLING_INTERVAL);

        return () => clearInterval(intervalId); // Cleanup on component unmount
    }, [liveTransactions]);

    function createLiveTransactionsRow(liveTransaction, i) {
        const classType = liveTransaction.type === 'Attack' ? 'table-danger' : 'table-success'
        return (
            <tr key={i} className={classType}>
                <td>{liveTransaction.date}</td>
                <td>{liveTransaction.time}</td>
                <td>{liveTransaction.transactionHash}</td>
                <td>{liveTransaction.gasPrice}</td>
                <td>{liveTransaction.ethTransferred}</td>
            </tr>
        );
    }


    return (
        <Col className={["justify-content-center", styles.searchResult].join(" ")}>
        {liveTransactions ? <>
            <Row><h3>Live transactions classification</h3></Row>
            <Row className="justify-content-center"><Table className={styles.resultTable}>
                <thead className="table-dark">
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Transaction hash</th>
                    <th>Gas Price</th>
                    <th>ETH Transferred</th>
                </tr>
                </thead>
                <tbody>
                {liveTransactions.map((liveTransaction, i) => createLiveTransactionsRow(liveTransaction, i))}
                </tbody>
            </Table></Row></>: <Spinner animation="border" variant="primary"/> }
        </Col>
    );
}

export default InsertionAttackLive;
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
            const sortedResult = response.sort((a, b) => a.time > b.time)
            setLiveTransactions(sortedResult);
        }, POLLING_INTERVAL);

        return () => clearInterval(intervalId); // Cleanup on component unmount
    }, [liveTransactions]);

    function createLiveTransactionsRow(liveTransaction, i) {
        const classType = liveTransaction.isAttack ? 'table-danger' : 'table-success'
        const etherscanLink = `https://etherscan.io/tx/${liveTransaction.transaction_hash}`
        return (
            <tr key={i} className={classType}>
                <td>{liveTransaction.date}</td>
                <td>{liveTransaction.time}</td>
                <td><a href={etherscanLink} target="_blank" rel="noreferrer">{liveTransaction.transaction_hash}</a></td>
                <td>{(Math.round(liveTransaction.gasPrice * 100) / 100).toFixed(2)}</td>
                <td>{(Math.round(liveTransaction.ethAmount * 10000000) / 10000000).toFixed(7)}</td>
            </tr>
        );
    }


    return (
        <Col className={["justify-content-center", styles.searchResult, styles.textCenter].join(" ")}>
        {liveTransactions ? <>
            <Row><h3>Live transactions classification</h3></Row>
            <Row className={"justify-content-center"}><Table className={styles.resultTable}>
                <thead className="table-dark">
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Transaction hash</th>
                    <th>Gas Price [GWei]</th>
                    <th>Transaction value [ETH]</th>
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
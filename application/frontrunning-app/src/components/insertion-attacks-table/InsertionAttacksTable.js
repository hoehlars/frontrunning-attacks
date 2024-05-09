import {useEffect, useState} from "react";
import {
    getInsertionAtkTable
} from "../../services/insertionAttackService";
import styles from './InsertionAttacksTable.module.css'
import {Col, Row, Spinner, Table} from "react-bootstrap";

function InsertionAttacksTable() {
    const [data, setData] = useState([]);
    const POLLING_INTERVAL = 10000;

    useEffect(() => {
        const intervalId = setInterval(async () => {
            const data = await getInsertionAtkTable();
            setData(data)
        }, POLLING_INTERVAL);
        return () => clearInterval(intervalId);
    }, [data]);

    function createLiveTransactionsRow(liveTransaction, i) {
        const etherscanLink = `https://etherscan.io/tx/${liveTransaction.transaction_hash}`
        const shortenedTransactionHash = liveTransaction.transaction_hash.slice(0, 20) + '...'
        return (
            <tr key={i} className='table-danger'>
                <td>{liveTransaction.date}</td>
                <td>{liveTransaction.time}</td>
                <td><a href={etherscanLink} target="_blank" rel="noreferrer">{shortenedTransactionHash}</a></td>
                <td>{(Math.round(liveTransaction.gasPrice * 100) / 100).toFixed(2)}</td>
                <td>{(Math.round(liveTransaction.ethAmount * 100) / 100).toFixed(2)}</td>
            </tr>
        );
    }

    return (
        <Col className={["justify-content-center", styles.searchResult, styles.textCenter].join(" ")}>
            {data.length > 0 ? <>
                <h3>Last 5 insertion attacks</h3>
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
                    {data.map((liveTransaction, i) => createLiveTransactionsRow(liveTransaction, i))}
                    </tbody>
                </Table></Row></>: <Spinner animation="border" variant="primary"/> }
        </Col>
    );
}

export default InsertionAttacksTable;
import styles from "./InsertionAttackModel.module.css"
import {useState} from "react";
import {
    getClassificationOfInsertionAttackModel
} from "../../services/insertionAttackService";
import {Button, Col, InputGroup, Row, Spinner} from "react-bootstrap";
import Form from "react-bootstrap/Form";
import {Tooltip} from 'react-tooltip'


function InsertionAttackModel() {
    const [transactionHash, setTransactionHash] = useState('');
    const [isSearching, setSearching] = useState(false);
    const [modelResult, setModelResult] = useState('');

    async function startSearching() {
        setSearching(true);
        setModelResult('');
        const response = await getClassificationOfInsertionAttackModel(transactionHash);
        setSearching(false);
        const result = response['attack'];
        result ? setModelResult('an attack!') : setModelResult('not an attack!');
    }

    return (
        <Col className="align-content-center">
            <Row>
                <Tooltip id="tooltip-transaction-search"/>
                <InputGroup data-tooltip-id="tooltip-transaction-search" data-tooltip-content="Insert a transaction hash here.
            As a result you will see if the transaction will be classified as an insertion attack or not."
                            className={[styles.searchBar, "mb-2"].join(" ")}>
                    <Form.Control
                        placeholder="Insert a transaction hash here"
                        aria-label="Block number"
                        aria-describedby="basic-addon2"
                        onChange={e => setTransactionHash(e.target.value)}
                    />
                    <Button variant="primary" id="button-addon2" onClick={startSearching}>
                        Search
                    </Button>
                </InputGroup>
                <Tooltip text="123"></Tooltip>
            </Row>
            <Row className={["justify-content-center", styles.searchResult].join(" ")}>
                {isSearching ? <Spinner animation="border" variant="primary"/> : null}
                {modelResult ? <p className={styles.searchResultText}>The transaction with the transaction hash {transactionHash} is {modelResult}</p> : null}
            </Row>
        </Col>);
}

export default InsertionAttackModel;
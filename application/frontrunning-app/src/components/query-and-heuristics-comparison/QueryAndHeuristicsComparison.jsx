import React, {useState} from "react";
import Container from "react-bootstrap/Container";
import {Alert, Button, Col, InputGroup, Row, Spinner, Table} from "react-bootstrap";
import {Tooltip} from "react-tooltip";
import Form from "react-bootstrap/Form";
import {
    getClassificationByModelAndHeuristics
} from "../../services/insertionAttackService";

const ModelFeaturesTable = ({ features }) => {
    return (
        <div className="mt-3">
            <h5 className="mt-4">Model Features</h5>
            <Table striped bordered hover size="sm">
                <thead>
                <tr>
                    <th>Feature</th>
                    <th>Value</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>Gas Price [GWei]</td>
                    <td>{features.gasPrice}</td>
                </tr>
                <tr>
                    <td>Mean Gas Price Last 10 Blocks [GWei]</td>
                    <td>{features.meanGasPriceLast10Blocks}</td>
                </tr>
                <tr>
                    <td>Std Gas Price Last 10 Blocks [GWei]</td>
                    <td>{features.stdGasPriceLast10Blocks}</td>
                </tr>
                <tr>
                    <td>Mean Gas Price Last 10 Blocks same EAO [GWei]</td>
                    <td>{features.meanGasPriceLast10BlocksSameEAO}</td>
                </tr>
                <tr>
                    <td>Std Gas Price Last 10 Blocks same EAO [GWei]</td>
                    <td>{features.stdGasPriceLast10BlocksSameEAO}</td>
                </tr>
                <tr>
                    <td>Used Gas Token</td>
                    <td>{features.usedGasToken.toString().toUpperCase()}</td>
                </tr>
                <tr>
                    <td>Predicted Gas Price [GWei]</td>
                    <td>{features.predictedGasPrice}</td>
                </tr>
                </tbody>
            </Table>
        </div>
    );
};

const TransactionForm = () => {
    const [transactionHash, setTransactionHash] = useState('');
    const [transactionInfo, setTransactionInfo] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true)

        const foundTransaction = await getClassificationByModelAndHeuristics(transactionHash)
        console.log(foundTransaction)

        if (foundTransaction) {
            setTransactionInfo(foundTransaction);
            setError(null);
        } else {
            setTransactionInfo(null);
            setError('Transaction does NOT exist!');
        }

        setIsLoading(false)
    };

    return (
        <Container>
            <Row className="text-center">
                <h4>Check Transaction Hash - Comparison Model vs. Heuristcs</h4>
            </Row>
            <Row className="justify-content-center" style={{ paddingTop: "10px"}}>
                <Tooltip id="tooltip-transaction-search"/>
                <InputGroup style={{ maxWidth: "75%"}} data-tooltip-id="tooltip-transaction-search" data-tooltip-content="Insert a transaction hash here.
            As a result our model and heuristics will check if the transaction is part of an attack."
                >
                    <Form.Control
                        placeholder="Insert a Transaction Hash here"
                        aria-label="Block number"
                        aria-describedby="basic-addon2"
                        onChange={e => setTransactionHash(e.target.value)}
                        style={{fontSize: "13px"}}
                    />
                    <Button variant="primary" id="button-addon2" onClick={handleSubmit}>
                        Check Transaction
                    </Button>
                </InputGroup>
            </Row>
            <Row className="justify-content-center mt-3">
                <Col md={9}>
                    {!isLoading && error && <Alert variant="danger" className="mt-3">{error}</Alert>}
                    {isLoading && (
                        <Col className="text-center mt-3">
                            <Spinner animation="border" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </Spinner>
                        </Col>
                    )}
                    {!isLoading && transactionInfo && (
                        <div >
                            <Row className="text-center">
                                <h6>Transaction found in Block Number:
                                    <a
                                        href={`https://etherscan.io/block/${transactionInfo.blockNumber}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        style={{marginLeft: "5px"}}
                                    >
                                        {transactionInfo.blockNumber}
                                    </a>
                                </h6>
                            </Row>
                            <Alert variant={transactionInfo.isModelAttack ? "warning" : "success"}>
                                The Model {transactionInfo.isModelAttack ? "classified" : "did NOT classify"} the transaction as an attack.
                            </Alert>
                            <Alert variant={transactionInfo.isHeuristicsAttack ? "warning" : "success"}>
                                The Heuristics {transactionInfo.isHeuristicsAttack ? "classified" : "did NOT classify"} the transaction as an attack.
                            </Alert>
                            <ModelFeaturesTable features={transactionInfo.modelFeatures}></ModelFeaturesTable>
                        </div>
                    )}
                </Col>
            </Row>
        </Container>
    );
};

export default TransactionForm;

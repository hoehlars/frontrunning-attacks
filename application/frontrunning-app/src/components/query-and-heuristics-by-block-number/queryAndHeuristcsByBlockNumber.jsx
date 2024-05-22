import React, {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from "react-bootstrap/Container";
import {Alert, Button, Col, InputGroup, Row, Spinner, Table} from "react-bootstrap";
import {Tooltip} from "react-tooltip";
import Form from "react-bootstrap/Form";
import {getAttackTransactionFromBlock} from "../../services/insertionAttackService";


const InsertionAttackTrioTable = ({ data }) => {
    const columnNames = ["Address", "Transaction Hash", "Gas Fees [GWei]", "Amount [USD]"];

    const transactions = [
        { name: 'Attack 1', data: data.attack1, className: 'table-danger' },
        { name: 'Victim', data: data.victim, className: 'table-success' },
        { name: 'Attack 2', data: data.attack2, className: 'table-danger' }
    ];

    function etherscanLink(type, hash) {

        return `https://etherscan.io/${type}/${hash}`
    }

    function sliceHash(hash) {
        return hash.slice(0,15) + '...' + hash.slice(-15)
    }

    return (
            <Table bordered hover>
                <thead className="table-dark">
                <tr>
                    <th></th>
                    {columnNames.map((columnName, index) => (
                        <th key={index} className="text-center font-weight-bold">{columnName}</th>
                    ))}
                </tr>
                </thead>
                <tbody>
                {transactions.map(({ name, data, className }) => (
                    <tr key={name} className={className}>
                        <td className="text-center" style={{minWidth: "90px", fontWeight: 'bold'}}>{name}</td>
                        <td><a href={etherscanLink('address', data.address)} target="_blank" rel="noreferrer">{sliceHash(data.address)}</a></td>
                        <td><a href={etherscanLink('tx', data.hash)} target="_blank" rel="noreferrer">{sliceHash(data.hash)}</a></td>
                        <td>{data.gasFees}</td>
                        <td>{data.amount} $</td>
                    </tr>
                ))}
                </tbody>
            </Table>
    );
};

const AssertionAttackInformation = ({values}) => {

    const InformationItem = ({label, value}) => (
        <div style={{marginBottom: '5px'}}>
            <div style={{fontWeight: 'bold'}}>{label}:</div>
            <div style={{border: '2px solid darkgray', padding: '5px'}}>{value}</div>
        </div>
    );

    const etherscanLink = `https://etherscan.io/address/${values.tokenAddress}`

    return (
        <div style={{flex: 1, paddingLeft: '10px'}}>
            <InformationItem label="Cost" value={values.cost + " $"}/>
            <InformationItem label="Profit" value={values.profit + " $"}/>
            <div style={{marginBottom: '5px'}}>
                <div style={{fontWeight: 'bold'}}>Token:</div>
                <a href={etherscanLink} target="_blank" rel="noopener noreferrer"
                   style={{border: '2px solid darkgray', padding: '5px', display: 'inline-block'}}>
                    {values.tokenName}
                </a>
            </div>
        </div>
    );
};

const InsertionAttackListItem = ({tableData, attackInformation}) => {
    return (
        <Container style={{border: "3px solid gray", marginTop: '5px'}}>
        <Row style={{marginTop: '10px'}}>
                <Col xs={10} style={{borderRight: "3px solid darkgray", marginBottom: '5px'}}>
                    <InsertionAttackTrioTable data={tableData} />
                </Col>
                <Col xs={2}>
                    <AssertionAttackInformation values={attackInformation} />
                </Col>
            </Row>
        </Container>
    );
};

const InsertionAttackList = ({ data }) => {

    if (!data || data.length === 0) {
        return(
            <Row className="justify-content-center">
                <Col className="text-center mt-3" style={{maxWidth: "50%"}}>
                    <Alert variant="alert alert-secondary" className="mt-3">No attacks found for the selected block!</Alert>
                </Col>
            </Row>
        );
    }

    return (
        <div className="overflow-auto" style={{ maxHeight: '400px', marginTop: '5px', marginBottom: '5px' }}>
            {data.map((item, index) => (
                <InsertionAttackListItem key={index} tableData={item.transactions} attackInformation={item.attackInformation} />
            ))}
        </div>
    );
};


function QueryAndHeuristcsByBlockNumber() {

    const [blockNumber, setBlockNumber] = useState('');
    const [data, setData] = useState(null)
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {

        setIsLoading(true);

        const data = await getAttackTransactionFromBlock(blockNumber)
        setData(data)

        setIsLoading(false);
    };

    return (
    <Container style={{minHeight: "450px"}}>
        <Row className="text-center">
            <h2>Search Front-running Attacks by Block-Number using Heuristics</h2>
        </Row>
        <Row className="justify-content-center" style={{ paddingTop: "10px"}}>
            <Tooltip id="tooltip-transaction-search"/>
            <InputGroup style={{ maxWidth: "30%"}} data-tooltip-id="tooltip-transaction-search" data-tooltip-content="Insert a block number here.
            As a result our heuristics will search the block for any insertion attacks."
                        >
                <Form.Control
                    placeholder="Insert a Blocknumber here"
                    aria-label="Block number"
                    aria-describedby="basic-addon2"
                    onChange={e => setBlockNumber(e.target.value)}
                />
                <Button variant="primary" id="button-addon2" onClick={handleSubmit}>
                    Search
                </Button>
            </InputGroup>
            <Tooltip text="123"></Tooltip>
        </Row>
        <Row>
        {isLoading ? (
            <Col className="text-center mt-3">
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            </Col> ) :
            data !== null ? (
            <Row>
                <InsertionAttackList data={data}/>
            </Row> ) :
                (
            <Row></Row>
                )
        }
        </Row>
    </Container>
    );
}

export default QueryAndHeuristcsByBlockNumber;
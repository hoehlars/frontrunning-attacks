import React, { useState } from 'react';
import {Container, Row, Col, InputGroup, Button, Spinner, Alert} from 'react-bootstrap';
import Plot from 'react-plotly.js';
import Form from "react-bootstrap/Form";
import {getCostProfitFromBlockRange} from "../../services/insertionAttackService";


const CostProfitChart = () => {

    const [blockNumberFrom, setBlockNumberFrom] = useState('');
    const [blockNumberTo, setBlockNumberTo] = useState('');
    const [chartData, setChartData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const isButtonDisabled = () => {
        const from = parseInt(blockNumberFrom, 10);
        const to = parseInt(blockNumberTo, 10);

        if (isNaN(from) || isNaN(to)) {
            return true;
        }

        const difference = to - from;
        return !(difference >= 0 && difference <= 100);
    };

    const handleSearch = async (e) => {

        setIsLoading(true);

        const data = await getCostProfitFromBlockRange(blockNumberFrom, blockNumberTo)
        console.log(data)

        if (data && data.length > 0) {
            const blockNumbers = data.map(item => item.blockNumber);
            const costs = data.map(item => item.cost);
            const profits = data.map(item => item.profit);

            setChartData({
                blockNumbers,
                costs,
                profits
            });
        } else {
            setChartData({});
        }

        setIsLoading(false);
    };



    return (
        <Container>
            <Row className="text-center">
                <h4>Profit and Cost by Block-Range</h4>
            </Row>
            <Row className="justify-content-center" style={{ paddingTop: "10px" , paddingLeft: "100px"}}>
                <InputGroup style={{ maxWidth: "85%" }}>
                    <Col>
                        <Form.Label style={{ fontSize: '0.8em' }}>FROM Block Number</Form.Label>
                        <Form.Control
                            placeholder="Insert a Blocknumber here"
                            aria-label="Block number"
                            aria-describedby="basic-addon2"
                            onChange={e => setBlockNumberFrom(e.target.value)}
                        />
                    </Col>
                    <Col>
                        <Form.Label style={{ fontSize: '0.8em' }}>TO Block Number</Form.Label>
                        <Form.Control
                        placeholder="Insert a Blocknumber here"
                        aria-label="Block number"
                        aria-describedby="basic-addon2"
                        onChange={e => setBlockNumberTo(e.target.value)}
                    />
                    </Col>
                    <Col className="d-flex align-items-end">
                        <Button
                            variant="primary"
                            id="button-addon2"
                            onClick={handleSearch}
                            disabled={isButtonDisabled()}
                        >
                            Search
                        </Button>
                    </Col>
                </InputGroup>
            </Row>
            <Row className="justify-content-center" style={{ paddingTop: "20px" }}>
                {isLoading ? (
                    <Col className="text-center mt-3">
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </Spinner>
                    </Col>
                ) : (
                    chartData !== null && (
                        <BarPlot chartData={chartData} />
                    )
                )}
            </Row>
        </Container>
    );
};

const BarPlot = ({ chartData }) => {

    if (!chartData || !chartData.blockNumbers || chartData.blockNumbers.length === 0) {
        return(
            <Row className="justify-content-center">
                <Col className="text-center mt-3" style={{maxWidth: "80%"}}>
                    <Alert variant="alert alert-secondary" className="mt-3">No attacks found for the selected block-range!</Alert>
                </Col>
            </Row>
        );
    }

    return (
        <Plot
            data={[
                {
                    x: chartData.blockNumbers,
                    y: chartData.costs,
                    type: 'bar',
                    name: 'Cost',
                    marker: { color: 'red' },
                },
                {
                    x: chartData.blockNumbers,
                    y: chartData.profits,
                    type: 'bar',
                    name: 'Profit',
                    marker: { color: 'green' },
                }
            ]}
            layout={{
                barmode: 'group',
                title: 'Profit and Cost by Block-Range',
                xaxis: {
                    title: 'Block Number',
                    tickformat: 'd',  // ensure block numbers showed as whole numbers
                },
                yaxis: {
                    title: {
                        text: 'Value [$]',
                        standoff: 20
                    },
                    tickprefix: '$'
                }
            }}
            config={{displayModeBar: false}}
            style={{ width: "100%", height: "100%" }}
        />
    );
};

export default CostProfitChart;
import {Col, Row} from "react-bootstrap";
import styles from './QueryAndHeuristics.module.css'
import Container from "react-bootstrap/Container";
import QueryAndHeuristcsByBlockNumber from "../query-and-heuristics-by-block-number/queryAndHeuristcsByBlockNumber";
import CostProfitChart from "../query-and-heuristics-chart/QueryAndHeurisitcsChart";
import TransactionForm from "../query-and-heuristics-comparison/QueryAndHeuristicsComparison";


function QueryAndHeuristics() {
    return (
        <Container fluid lg={2} className="m-0">
            <Row className={[styles.bottomPaneBorder].join(" ")}>
                <QueryAndHeuristcsByBlockNumber></QueryAndHeuristcsByBlockNumber>
            </Row>
            <Row className={styles.minHeight}>
                <Col className={[styles.topPaneLeftBorder].join(" ")}>
                    <CostProfitChart></CostProfitChart>
                </Col>
                <Col>
                    <TransactionForm></TransactionForm>
                </Col>
            </Row>
        </Container>
    );
}

export default QueryAndHeuristics;
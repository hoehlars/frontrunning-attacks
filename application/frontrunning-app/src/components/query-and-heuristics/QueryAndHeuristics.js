import {Col, Row} from "react-bootstrap";
import InsertionAttackModel from "../insertion-attacks-model/InsertionAttackModel";
import styles from './QueryAndHeuristics.module.css'
import Container from "react-bootstrap/Container";


function QueryAndHeuristics() {
    return (
        <Container fluid lg={2} className="m-0">
            <Row className={styles.minHeight}>
                <Col className={[styles.topPaneLeftBorder].join(" ")}></Col>
                <Col></Col>
            </Row>
            <Row className={[styles.bottomPaneBorder].join(" ")}>

            </Row>
        </Container>
    );
}

export default QueryAndHeuristics;
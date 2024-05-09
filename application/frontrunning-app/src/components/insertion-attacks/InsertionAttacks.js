import {Col, Row} from "react-bootstrap";
import InsertionAttackLive from "../insertion-attacks-live/InsertionAttackLive";
import styles from './InsertionAttacks.module.css'
import Container from "react-bootstrap/Container";
import InsertionAttacksTimeSeries from "../insertion-attacks-time-series/InsertionAttacksTimeSeries";
import InsertionAttacksTable from "../insertion-attacks-table/InsertionAttacksTable";


function InsertionAttacks() {
    return (
        <Container fluid lg={2} className="m-0">
            <Row className={styles.minHeight}>
                <InsertionAttackLive/>
            </Row>
            <Row className={[styles.bottomPaneBorder].join(" ")}>
                <Col className={[styles.bottomPaneLeftBorder].join(" ")}><InsertionAttacksTimeSeries /></Col>
                <Col><InsertionAttacksTable /></Col>
            </Row>
        </Container>
    );
}

export default InsertionAttacks;
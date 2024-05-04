import {Col, Row} from "react-bootstrap";
import InsertionAttackModel from "../insertion-attacks-model/InsertionAttackModel";
import InsertionAttackHeuristics from "../insertion-attacks-heuristics/InsertionAttackHeuristics";
import InsertionAttackLive from "../insertion-attacks-live/InsertionAttackLive";
import styles from './InsertionAttacks.module.css'
import Container from "react-bootstrap/Container";


function InsertionAttacks() {
    return (
        <Container fluid lg={2} className="m-0">
            <Row className={styles.minHeight}>
                <Col className={[styles.topPaneLeftBorder].join(" ")}><InsertionAttackModel /></Col>
                <Col><InsertionAttackHeuristics /></Col>
            </Row>
            <Row className={[styles.bottomPaneBorder].join(" ")}>
                <InsertionAttackLive />
            </Row>
        </Container>
    );
}
export default InsertionAttacks;
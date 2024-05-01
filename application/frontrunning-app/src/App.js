import './App.css';
import NavBar from "./components/NavBar/navbar";
import ScreenLeftSide from "./components/screen-left-side/screen-left-side";
import ScreenRightSide from "./components/screen-right-side/screen-right-side";
import {Col, Row} from "react-bootstrap";

function App() {
  return (
    <div className="App">
      <NavBar />
      <Row>
          <Col><ScreenLeftSide/></Col>
          <Col><ScreenRightSide/></Col>
      </Row>
    </div>
  );
}

export default App;

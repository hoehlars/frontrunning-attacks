import "./screen-right-side-styles.css"
import {Button, InputGroup} from "react-bootstrap";
import Form from 'react-bootstrap/Form';
import {useState} from "react";
function ScreenRightSide() {
    const [blockNumber, setBlockNumber] = useState('');
    const [searchingBlockNumber, setSearchingBlockNumber] = useState('');
    const [isSearching, setSearching] = useState(false);

    function startSearching() {
        setSearching(true);
        setSearchingBlockNumber(blockNumber);
    }

    return (
        <div className={"rightSide"}>
            <InputGroup className="mb-3" style={{width: "50%"}}>
                <Form.Control
                    placeholder="Block number"
                    aria-label="Block number"
                    aria-describedby="basic-addon2"
                    onChange={e => setBlockNumber(e.target.value)}
                />
                <Button variant="primary" id="button-addon2" onClick={e => startSearching()}>
                    Button
                </Button>
            </InputGroup>
            {isSearching ? <p>Searching for block number {searchingBlockNumber}</p> : null}
        </div>
    );
}
export default ScreenRightSide;
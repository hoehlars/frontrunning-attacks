import './App.css';
import InsertionAttacks from "./components/insertion-attacks/InsertionAttacks";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import QueryAndHeuristics from "./components/query-and-heuristics/QueryAndHeuristics";
import NavBar from "./components/NavBar/navbar";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<>
                    <NavBar/>
                    <InsertionAttacks/>
                </>}/>
                <Route path="/queryAndHeuristics" element={
                    <>
                        <NavBar/>
                        <QueryAndHeuristics/>
                    </>}/>
            </Routes>
        </Router>
    );
}

export default App;

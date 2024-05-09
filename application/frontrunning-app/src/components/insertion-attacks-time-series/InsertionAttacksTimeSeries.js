import Plot from 'react-plotly.js';
import {useEffect, useState} from "react";
import {
    getInsertionAtkTimeSeries,
} from "../../services/insertionAttackService";
import styles from './InsertionAttacksTimeSeries.module.css'
import {Row, Spinner} from "react-bootstrap";

function InsertionAttacksTimeSeries() {
    const [xData, setXData] = useState([]);
    const [yData, setYData] = useState([]);

    useEffect(() => {
        async function fetchTimeSeries() {
            const timeSeries = await getInsertionAtkTimeSeries()

            timeSeries.forEach(timePoint => setXData([...xData, new Date(timePoint._id)
                .toLocaleDateString('de-CH', {
                day: '2-digit',
                month: '2-digit',
                year: '2-digit'
            })]));
            timeSeries.forEach(timePoint => setYData([...yData, timePoint.count]));
        }

        fetchTimeSeries()
    }, [xData, yData]);

    return (
        <Row className={["justify-content-center"].join(" ")}>
            {xData.length > 0 ?
            <Plot
                  data={[
                      {
                          x: xData,
                          y: yData,
                          type: 'scatter',
                          mode: 'lines+markers',
                          marker: {color: 'red'},
                      },
                      {type: 'bar'},
                  ]}
                  layout={{
                      title: 'Time Series Insertion Attack', xaxis: {
                          tickvals: xData
                      }
                  }}
                  style={{marginLeft: 'auto', marginRight: 'auto'}}
            /> : <Spinner className={styles.spinner} animation="border" variant="primary"/>}
        </Row>
    );
}

export default InsertionAttacksTimeSeries;
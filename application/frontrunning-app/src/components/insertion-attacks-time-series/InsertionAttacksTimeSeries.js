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
            const timeSeries = await getInsertionAtkTimeSeries();

            const xNew = [];
            const yNew = [];

            timeSeries.forEach(timePoint => xNew.push(new Date(timePoint._id)
                .toLocaleDateString('de-CH', {
                    day: '2-digit',
                    month: '2-digit',
                    year: '2-digit'
                })));
            timeSeries.forEach(timePoint => yNew.push(timePoint.count));
            setXData(xNew);
            setYData(yNew);
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
                          type: 'bar',
                          mode: 'markers',
                          marker: {color: 'red'},
                      },
                  ]}
                  layout={{
                      title: 'Time Series Insertion Attack',
                      xaxis: {
                          tickvals: xData
                      },
                      yaxis: {
                          range: [0, 100]
                      },
                  }}
                  style={{marginLeft: 'auto', marginRight: 'auto'}}
            /> : <Spinner className={styles.spinner} animation="border" variant="primary"/>}
        </Row>
    );
}

export default InsertionAttacksTimeSeries;
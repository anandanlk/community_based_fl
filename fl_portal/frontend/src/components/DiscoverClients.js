import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/DiscoverClients.css';

function DiscoverClients() {
    const [clientIPs, setClientIPs] = useState([]);
    const [message, setMessage] = useState('');
    const [metrics, setMetrics] = useState(null);
    const [logs, setLogs] = useState('');
    const [executionTime, setExecutionTime] = useState(null);
    const [showLogs, setShowLogs] = useState(false);

    useEffect(() => {
        const fetchClientIPs = async () => {
            try {
                const response = await API.get('/discover_clients', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setClientIPs(response.data);
            } catch (error) {
                console.error('Error fetching client IPs:', error);
            }
        };
        fetchClientIPs();
    }, []);

    const handleInitiateFL = async () => {
        setMessage('FL Training is initiated, it will take some time, please wait.');
        try {
            const response = await API.post('/initiate_fl', {}, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            });
            const result = response.data;
            setMetrics(result.metrics);
            setLogs(result.logs);
            setExecutionTime(result.execution_time);
            setMessage('');
        } catch (error) {
            console.error('Error initiating FL:', error);
            setMessage('Error initiating FL.');
        }
    };

    const renderMetricsTable = () => {
        if (!metrics) return null;
        return (
            <table className="table">
                <thead>
                    <tr>
                        {Object.keys(metrics).map((key, index) => (
                            <th className="th" key={index}>{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {metrics.Round.map((_, rowIndex) => (
                        <tr key={rowIndex}>
                            {Object.keys(metrics).map((key, colIndex) => (
                                <td className="td" key={colIndex}>{metrics[key][rowIndex]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div>
            <h2>Discovered Clients</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th className="th">Client IP</th>
                    </tr>
                </thead>
                <tbody>
                    {clientIPs.map((ip, index) => (
                        <tr key={index}>
                            <td className="td">{ip}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {!metrics && (
                <button onClick={handleInitiateFL} className="button">Initiate FL</button>
            )}
            {message && <p className="center">{message}</p>}
            {executionTime && (
                <div className="center">
                    <p>Time taken to complete FL Training: {executionTime}</p>
                </div>
            )}
            {metrics && renderMetricsTable()}
            {metrics && (
                <div className="center">
                    <button 
                        onClick={() => setShowLogs(!showLogs)} 
                        className="link-button">
                        {showLogs ? 'Hide Logs' : 'Show Logs'}
                    </button>
                    {showLogs && <pre>{logs}</pre>}
                </div>
            )}
        </div>
    );
}

export default DiscoverClients;
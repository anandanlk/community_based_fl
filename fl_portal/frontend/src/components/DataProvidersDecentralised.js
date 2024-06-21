import React, { useEffect, useState } from 'react';
import API from '../api';

function DataProvidersDecentralised() {
    const [dataProviders, setDataProviders] = useState([]);

    useEffect(() => {
        const fetchDataProviders = async () => {
            try {
                const response = await API.get('/data_providers_decentralised', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setDataProviders(response.data);
            } catch (error) {
                console.error('Error fetching data providers:', error);
            }
        };
        fetchDataProviders();
    }, []);

    return (
        <div>
            <h2>Data Providers (Decentralised)</h2>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
                <thead>
                    <tr>
                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Username</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Type</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Group</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Topology</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Email</th>
                    </tr>
                </thead>
                <tbody>
                    {dataProviders.map((provider) => (
                        <tr key={provider.id}>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{provider.username}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{provider.type}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{provider.group}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{provider.topology}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{provider.email}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DataProvidersDecentralised;

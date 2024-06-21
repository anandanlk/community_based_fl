import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import DataProviders from './components/DataProviders';
import DataProvidersDecentralised from './components/DataProvidersDecentralised';
import DataProvidersCentralised from './components/DataProvidersCentralised';
import RegisteredClients from './components/DiscoverClients';
import DataScientists from './components/DataScientists';

function App() {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/data-providers" element={<DataProviders />} />
                    <Route path="/data-scientists" element={<DataScientists />} />
                    <Route path="/data-providers-decentralised" element={<DataProvidersDecentralised />} />
                    <Route path="/data-providers-centralised" element={<DataProvidersCentralised />} />
                    <Route path="*" element={<Navigate to="/login" />} />
                    <Route path="/discover-clients" element={<RegisteredClients />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
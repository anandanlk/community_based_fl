import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API from '../api';
import '../styles/Home.css';

function Home() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                await API.get('/', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Failed to load data');
                navigate('/login');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <div>
            <header className="header">
                <h1>Community FL</h1>
                <button onClick={handleLogout} className="logout-button">Logout</button>
            </header>
            <nav className="nav">
                <ul className="ul">
                    <li><Link to="/data-scientists">Data Scientists</Link></li>
                    <li><Link to="/discover-clients">Discover Data Providers</Link></li>
                </ul>
            </nav>
            <div className="center">
                {loading ? <p>Loading...</p> : error ? <p>{error}</p> : null}
            </div>
        </div>
    );
}

export default Home;

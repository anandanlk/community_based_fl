import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        type: '',
        group: '',
        topology: '',
        password: '',
        email: '',
    });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await API.post('/register', formData);
            navigate('/login');
        } catch (error) {
            console.error('Registration failed:', error);
            setError('Registration failed. Please check your inputs.');
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <form onSubmit={handleRegister} style={{ width: '300px', textAlign: 'center' }}>
                <h2>Register</h2>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <div style={{ marginBottom: '10px' }}>
                    <label>Username</label>
                    <input
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', marginTop: '5px' }}
                    />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label>Type</label>
                    <select
                        name="type"
                        value={formData.type}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', marginTop: '5px' }}
                    >
                        <option value="">Select Type</option>
                        <option value="Data Provider">Data Provider</option>
                        <option value="Data Scientist">Data Scientist</option>
                    </select>
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label>Group</label>
                    <input
                        type="text"
                        name="group"
                        value={formData.group}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', marginTop: '5px' }}
                    />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label>Topology</label>
                    <select
                        name="topology"
                        value={formData.topology}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', marginTop: '5px' }}
                    >
                        <option value="">Select Topology</option>
                        <option value="Decentralised">Decentralised</option>
                        <option value="Centralised">Centralised</option>
                    </select>
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', marginTop: '5px' }}
                    />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label>Email</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', marginTop: '5px' }}
                    />
                </div>
                <button type="submit" style={{ width: '100%' }}>Register</button>
            </form>
        </div>
    );
}

export default Register;
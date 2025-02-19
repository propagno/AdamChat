import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();
  const [userToken, setUserToken] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    } else {
      setUserToken(token);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div style={{ margin: '20px' }}>
      <h2>Dashboard</h2>
      <p>Você está logado! Seu token é: {userToken}</p>
      <button onClick={handleLogout}>Sair</button>
    </div>
  );
}

export default Dashboard;

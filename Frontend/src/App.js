// src/App.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCodeFromUrl, exchangeCodeForToken, login } from './services/auth';

const App = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const code = getCodeFromUrl();
        if (code) {
            exchangeCodeForToken(code).then(() => {
                window.history.replaceState({}, document.title, "/");
                navigate('/main');
            });
        } else {
            // Se não houver token, redireciona para o Cognito
            const token = localStorage.getItem('id_token');
            if (!token) {
                login();
            }
        }
    }, [navigate]);

    return (
        <div>
            <h1>AdamChat</h1>
        </div>
    );
};

export default App;

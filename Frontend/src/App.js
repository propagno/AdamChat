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
                // Limpa a URL removendo o código
                window.history.replaceState({}, document.title, "/");
                // Redireciona para a rota principal
                navigate('/main');
            });
        }
    }, [navigate]);

    return (
        <div>
            <h1>AdamChat</h1>
            <button onClick={login}>Login</button>
        </div>
    );
};

export default App;

// src/App.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCodeFromUrl, exchangeCodeForToken, login } from './services/auth';

const App = () => {
    const navigate = useNavigate();

    useEffect(() => {
      console.log("App carregado");
      const code = getCodeFromUrl();
      console.log("Código na URL:", code);
      if (code) {
          console.log("Trocando código por token...");
          exchangeCodeForToken(code).then(() => {
              window.history.replaceState({}, document.title, "/");
              navigate('/main');
          });
      } else {
          const token = localStorage.getItem('id_token');
          console.log("Token no localStorage:", token);
          if (!token) {
              console.log("Nenhum token encontrado, redirecionando para o Cognito...");
              login(); // Deve redirecionar para o Cognito
          } else {
              console.log("Token encontrado, redirecionando para /main");
              navigate('/main');
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

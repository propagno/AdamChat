import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authService from '../../services/authService';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Por favor, preencha todos os campos.');
      return;
    }

    try {
      const response = await authService.login(email, password);
      if (response.status === 'success') {
        localStorage.setItem('token', response.token);
        navigate('/dashboard');
      } else if (response.status === 'fail') {
        setError(response.message);
      }
    } catch (err) {
      setError('Erro ao tentar logar. Tente novamente.');
    }
  };

  return (
    <div style={{ margin: '20px' }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            placeholder="Digite seu email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <br />
        <div>
          <label>Senha:</label>
          <input
            type="password"
            placeholder="Digite sua senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <br />
        <button type="submit">Entrar</button>
      </form>
      <p>
        Não possui conta? <Link to="/register">Registre-se</Link>
      </p>
    </div>
  );
}

export default Login;

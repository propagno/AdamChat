import React, { useState } from "react";
import { login } from "../../services/authService";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const result = await login(email, password);
      if (result.error) {
        setError(result.error);
      } else {
        console.log("Login bem-sucedido", result);
      }
    } catch (err) {
      setError("Erro na requisição de login.");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Senha" onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Entrar</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
}

export default Login;

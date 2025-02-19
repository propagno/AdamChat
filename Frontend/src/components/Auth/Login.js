import React, { useState } from "react";
import { login } from "../services/api";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        const response = await login(username, password);
        if (response.error) {
            setError(response.error);
        } else {
            localStorage.setItem("token", response.token);
            window.location.href = "/dashboard";
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
                <input type="password" placeholder="Senha" onChange={(e) => setPassword(e.target.value)} />
                <button type="submit">Entrar</button>
            </form>
            {error && <p>{error}</p>}
        </div>
    );
}

export default Login;

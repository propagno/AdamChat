// Exemplo de serviço de autenticação para o SPA
// Altere API_URL para o endpoint correto do seu backend
const API_URL = "https://api.https://d273teevyftonl.cloudfront.net";

export async function login(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    return response.json();
  }
  
  export async function register(email, password) {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    return response.json();
  }
  
  // Agrupa as funções em um objeto e exporta como default:
  const authService = { login, register };
  export default authService;
  
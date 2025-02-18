const API_URL = 'http://localhost:5000'; // Altere para o URL do seu backend

const login = async (email, password) => {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    return await response.json();
  } catch (error) {
    return { error: 'Failed to connect to server' };
  }
};

export default {
  login,
};
const API_URL = 'http://localhost:5000'; // Atualize para a URL do seu backend

const authService = {
  login: async (email, password) => {
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      return await response.json();
    } catch (error) {
      console.error('Erro na requisição de login:', error);
      throw error;
    }
  },
  register: async (name, email, password) => {
    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, password })
      });
      return await response.json();
    } catch (error) {
      console.error('Erro na requisição de registro:', error);
      throw error;
    }
  }
};

export default authService;

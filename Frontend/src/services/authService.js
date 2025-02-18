import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Ajuste conforme necessário

const register = (email, password) => {
  return axios.post(`${API_URL}/register`, { email, password });
};

const login = (email, password) => {
  return axios.post(`${API_URL}/login`, { email, password });
};

export default {
  register,
  login,
};
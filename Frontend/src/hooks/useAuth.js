// src/services/auth.js
const cognitoDomain = process.env.REACT_APP_COGNITO_DOMAIN; // https://us-east-2m4hvqq1nu.auth.us-east-2.amazoncognito.com
const clientId = process.env.REACT_APP_CLIENT_ID; // 2iatr116il9ptd81nc8fq3l11h
const redirectUri = process.env.REACT_APP_REDIRECT_URI; // https://d273teevyftonl.cloudfront.net

export const login = () => {
  window.location.href = `${cognitoDomain}/login?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}`;
};

// Outras funções (getCodeFromUrl, exchangeCodeForToken) seguem aqui...

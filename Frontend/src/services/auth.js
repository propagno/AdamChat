// src/services/auth.js
const cognitoDomain = process.env.REACT_APP_COGNITO_DOMAIN;
const clientId = process.env.REACT_APP_CLIENT_ID;
const redirectUri = process.env.REACT_APP_REDIRECT_URI;

export const getCodeFromUrl = () => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('code');
};

export const exchangeCodeForToken = async (code) => {
    const tokenEndpoint = `${cognitoDomain}/oauth2/token`;

    const body = new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: clientId,
        redirect_uri: redirectUri,
        code: code
    });

    const response = await fetch(tokenEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body.toString()
    });

    const data = await response.json();
    localStorage.setItem('id_token', data.id_token);
    localStorage.setItem('access_token', data.access_token);
};

export const login = () => {
    window.location.href = `${cognitoDomain}/login?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}`;
};

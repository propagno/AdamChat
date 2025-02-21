export const login = () => {
    const cognitoDomain = process.env.REACT_APP_COGNITO_DOMAIN; // ex.: "https://us-east-2m4hvqq1nu.auth.us-east-2.amazoncognito.com"
    const clientId = process.env.REACT_APP_CLIENT_ID;           // ex.: "2iatr116il9ptd81nc8fq3l11h"
    const redirectUri = process.env.REACT_APP_REDIRECT_URI;       // ex.: "https://d273teevyftonl.cloudfront.net"
    const loginUrl = `${cognitoDomain}/login?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}`;
    console.log("Redirecionando para:", loginUrl);
    window.location.href = loginUrl;
};

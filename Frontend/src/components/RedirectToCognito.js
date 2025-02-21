// src/components/RedirectToCognito.js
import { useEffect } from 'react';
import { login } from '../services/auth';

const RedirectToCognito = () => {
    useEffect(() => {
        login();
    }, []);

    return null;
};

export default RedirectToCognito;

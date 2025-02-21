// src/Root.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import MainPage from './pages/MainPage';
import PrivateRoute from './components/PrivateRoute';
import RedirectToCognito from './components/RedirectToCognito';

const Root = () => (
    <Router>
        <Routes>
            <Route path="/" element={<App />} />
            <Route path="/login" element={<RedirectToCognito />} />
            <Route
                path="/main"
                element={
                    <PrivateRoute>
                        <MainPage />
                    </PrivateRoute>
                }
            />
        </Routes>
    </Router>
);

export default Root;

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/App';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider } from './features/auth/AuthContext';

ReactDOM.createRoot(document.getElementById('app')!).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID!}>
      <AuthProvider>
        <App />
      </AuthProvider>
    </GoogleOAuthProvider>
  </React.StrictMode>
);

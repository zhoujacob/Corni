import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../AuthContext';

const GoogleLoginButton = () => {
  const { setAccessToken } = useAuth();

  return (
    <GoogleLogin
      onSuccess={async credentialResponse => {
        const idToken = credentialResponse.credential;

        const res = await fetch('http://localhost:8000/api/auth/google-login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token: idToken }),
        });

        if (!res.ok) {
          const errorText = await res.text();
          console.error('Server error:', errorText);
          return;
        }

        const data = await res.json();
        setAccessToken(data.access);
        console.log('Django tokens:', data);
      }}
      onError={() => {
        console.log('Google login failed');
      }}
    />
  );
};

export default GoogleLoginButton;

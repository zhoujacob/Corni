import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../AuthContext';
import { googleLogin } from '../../../api/authApi';

const GoogleLoginButton = () => {
  const { setAccessToken } = useAuth();

  return (
    <GoogleLogin
      onSuccess={async credentialResponse => {
        try {
          const idToken = credentialResponse.credential;
          const data = await googleLogin(idToken!);
          setAccessToken(data.access);
          console.log('Django tokens:', data);
        } catch (err) {
          console.error(err);
        }
      }}
      onError={() => {
        console.error('Google login failed');
      }}
    />
  );
};

export default GoogleLoginButton;

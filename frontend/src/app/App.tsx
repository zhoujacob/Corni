import GoogleLoginButton from '../features/auth/components/GoogleLoginButton';
import { useAuth } from '../features/auth/AuthContext';
import { Routes, Route } from 'react-router';

function App() {
  const { accessToken } = useAuth();

  return (
    <Routes>
      <Route
        path="/"
        element={
          <div style={{ textAlign: 'center', marginTop: '4rem' }}>
            <h1>Corni</h1>
            {!accessToken ? (
              <>
                <p>Please sign in with Google to continue.</p>
                <GoogleLoginButton />
              </>
            ) : (
              <>
                <p>✅ Logged in successfully!</p>
                <code>{accessToken.slice(0, 40)}...</code>
              </>
            )}
          </div>
        }
      />
    </Routes>
  );
}

export default App;

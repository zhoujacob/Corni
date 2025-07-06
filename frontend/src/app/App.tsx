import GoogleLoginButton from '../features/auth/components/GoogleLoginButton';
import { useAuth } from '../features/auth/AuthContext';
import LoginPage from '../pages/LoginPage';
import RequireAuth from '../shared/RequireAuth';
import DashboardPage from '../pages/DashboardPage';
import { Routes, Route } from 'react-router';

function App() {
  const { accessToken } = useAuth();

  return (
    <>
    <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <DashboardPage />
            </RequireAuth>
          }
        />
      </Routes>
    </>
  );
}

export default App;

import { Routes, Route } from 'react-router';
import { useAuth } from '../features/auth/AuthContext';
import LoginPage from '../pages/LoginPage';
import RequireAuth from '../shared/RequireAuth';
import DashboardPage from '../pages/DashboardPage';
import Navbar from '../shared/Navbar';
import { ROUTES } from './routes/path';


function App() {
  const { accessToken } = useAuth();
  return (
    <>
    {accessToken && <Navbar />}
    <Routes>
        <Route path={ROUTES.LOGIN} element={<LoginPage />} />
        <Route
          path={ROUTES.DASHBOARD}
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

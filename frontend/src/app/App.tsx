import { Routes, Route } from 'react-router';
import { useAuth } from '../features/auth/AuthContext';
import LoginPage from '../pages/LoginPage';
import RequireAuth from '../shared/RequireAuth';
import DashboardPage from '../pages/DashboardPage';
import Navbar from '../shared/Navbar';


function App() {
  const { accessToken } = useAuth();
  return (
    <>
    {accessToken && <Navbar />}
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

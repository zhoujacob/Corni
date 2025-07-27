import { Routes, Route } from 'react-router';
import { useAuth } from '../features/auth/AuthContext';
import RequireAuth from '../shared/RequireAuth';
import Navbar from '../shared/Navbar';

import { ROUTES } from './routes/path';

import LoginPage from '../pages/LoginPage';
import DashboardPage from '../pages/DashboardPage';
import MovieDetailsPage from '../pages/MovieDetails';


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
        <Route
          path={ROUTES.MY_MOVIES}
          element={
            <RequireAuth>
              <MovieDetailsPage />
            </RequireAuth>
          }
        />
      </Routes>
      <footer style={{ textAlign: 'center', padding: '1rem', fontSize: '0.9rem' }}>
        <p>
          This product uses the <a href="https://www.themoviedb.org" target="_blank" rel="noreferrer">TMDB API</a> but is not endorsed or certified by TMDB.
        </p>
      </footer>
    </>
  );
}

export default App;

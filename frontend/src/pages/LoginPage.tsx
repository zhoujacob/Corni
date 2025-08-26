import { useAuth } from '../features/auth/AuthContext'
import GoogleLoginButton from '../features/auth/components/GoogleLoginButton'
import DevLoginButton from '../features/auth/components/DevLoginButton'
import { Navigate } from 'react-router-dom'
import { ROUTES } from '../app/routes/path'

export default function LoginPage() {
  const { accessToken, user } = useAuth()
  const hideGoogle = import.meta.env.VITE_HIDE_GOOGLE_LOGIN === 'true'

  // If already logged in, redirect to dashboard
  if (accessToken) {
    return <Navigate to={ROUTES.DASHBOARD} replace />;
  }

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        gap: '1.5rem'
      }}
    >
      <h1>Welcome to Corni</h1>
      <p>Please sign in to continue.</p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center', width: '100%', maxWidth: 420 }}>
        {!hideGoogle && <GoogleLoginButton />}
        {!hideGoogle && (
          <div style={{ display: 'flex', alignItems: 'center', width: '100%', gap: '0.75rem' }}>
            <div style={{ flex: 1, height: 1, background: '#eee' }} />
            <span style={{ color: '#777', fontSize: 12 }}>or</span>
            <div style={{ flex: 1, height: 1, background: '#eee' }} />
          </div>
        )}
        <DevLoginButton />
      </div>
    </div>
  )
}

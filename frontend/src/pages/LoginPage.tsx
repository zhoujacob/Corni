import { useAuth } from '../features/auth/AuthContext'
import GoogleLoginButton from '../features/auth/components/GoogleLoginButton'
import { Navigate } from 'react-router-dom'
import { ROUTES } from '../app/routes/path'

export default function LoginPage() {
  const { accessToken } = useAuth()

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
      <p>Please sign in with your Google account to continue.</p>
      <GoogleLoginButton />
    </div>
  )
}

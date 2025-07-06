// src/components/Navbar.tsx
import { Link } from 'react-router-dom'
import { useAuth } from '../features/auth/AuthContext'

export default function Navbar() {
  const { user, setAccessToken } = useAuth()

  return (
    <nav
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        padding: '1rem',
        borderBottom: '1px solid #eee'
      }}
    >
      <Link to="/">Home</Link>
      {user ? (
        <div>
          <span style={{ marginRight: '1rem' }}>{user.email}</span>
          <button onClick={() => setAccessToken(null)}>Logout</button>
        </div>
      ) : null}
    </nav>
  )
}

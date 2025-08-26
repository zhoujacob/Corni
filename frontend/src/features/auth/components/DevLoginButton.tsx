import { useState } from 'react';
import { useAuth } from '../AuthContext';
import { devLogin } from '../../../api/authApi';

export default function DevLoginButton() {
  const { setAccessToken } = useAuth();
  const [email, setEmail] = useState('dev@example.com');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDevLogin = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await devLogin(email.trim());
      setAccessToken(data.access);
    } catch (e: any) {
      setError(e?.message || 'Dev login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', width: '100%', maxWidth: 360 }}>
      <label htmlFor="dev-email" style={{ fontSize: 14, color: '#555' }}>Developer email</label>
      <input
        id="dev-email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="dev@example.com"
        style={{ padding: '0.5rem 0.75rem', border: '1px solid #ddd', borderRadius: 6 }}
      />
      <button onClick={onDevLogin} disabled={loading} style={{ padding: '0.5rem 0.75rem' }}>
        {loading ? 'Signing in…' : 'Sign in as Developer'}
      </button>
      {error ? <div style={{ color: 'crimson', fontSize: 12 }}>{error}</div> : null}
      <div style={{ fontSize: 12, color: '#777' }}>
        Works only in local dev (DEBUG). Creates or reuses a local test user and returns JWT.
      </div>
    </div>
  );
}


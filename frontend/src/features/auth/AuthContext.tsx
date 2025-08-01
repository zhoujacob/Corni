import { createContext, useContext, useState, useEffect } from 'react';
import type { AuthContextType } from '../../types/auth';
import type { User } from '../../types/user';
import { fetchUserProfile } from '../../api/authApi';

// contextAPI
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null)

  const isMock = import.meta.env.VITE_MOCK_AUTH === 'true';

  // Whenever we get a new token, fetch the profile
  useEffect(() => {
    // Local Testing
    if (isMock) {
      const mockUser: User = {
        id: 1,
        username: "mockuser",
        email: "mockuser@example.com",
        first_name: "Mocky",
        last_name: "Tester",
      };
      setUser(mockUser);
      setAccessToken("mock-token");
      return;
    }

    // Real Auth
    if (!accessToken) {
      setUser(null);
      return;
    }

    fetchUserProfile(accessToken)
      .then(setUser)
      .catch(() => {
        setAccessToken(null);
        setUser(null);
      });
  }, [accessToken, isMock]);
  console.log(user)

  return (
    <AuthContext.Provider value={{ accessToken, setAccessToken, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
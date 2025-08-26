import type { User } from '../types/user';

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function googleLogin(idToken: string): Promise<{ access: string; refresh: string }> {
  const res = await fetch(`${BASE_URL}/api/auth/google-login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: idToken }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Login failed: ${errorText}`);
  }

  return res.json();
}

export async function devLogin(email: string): Promise<{ access: string; refresh: string }> {
  const res = await fetch(`${BASE_URL}/api/auth/dev/login-as/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Dev login failed: ${errorText}`);
  }
  
  const data = await res.json();
  return { access: data.access, refresh: data.refresh };
}

export async function fetchUserProfile(token: string): Promise<User> {
  const res = await fetch(`${BASE_URL}/api/auth/me/`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error);
  }

  return res.json();
}

// src/components/RequireAuth.tsx
import { Navigate } from 'react-router-dom'
import { useAuth } from '../features/auth/AuthContext'
import React from 'react';

export default function RequireAuth({ children, }: { children: React.ReactNode; }) {
  const { accessToken } = useAuth()
  return accessToken ? children : <Navigate to="/" replace />
}

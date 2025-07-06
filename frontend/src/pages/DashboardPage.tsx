import { useAuth } from "../features/auth/AuthContext";

export default function DashboardPage({}) {
    const { user } = useAuth()

    if (!user) {
    return <p>Loading your profile…</p>
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Dashboard</h1>
      <p>Hi {user.first_name}</p>

    </div>
  )
}
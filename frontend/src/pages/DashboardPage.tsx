import { useAuth } from "../features/auth/AuthContext";
import DashboardCard from "../shared/DashboardCard";
import styles from './DashboardPage.module.css';

export default function DashboardPage() {
  const { user } = useAuth();

  if (!user) {
    return <p>Loading your profile…</p>;
  }

  return (
    <div className={styles.wrapper}>
      <h1>Dashboard</h1>
      <p>Hi {user.first_name}</p>

      <div className={styles.grid}>
        <DashboardCard title="My Groups">
          <p>View and manage your movie groups.</p>
        </DashboardCard>
        <DashboardCard title="My Movies">
          <p>Rate or review movies you've watched.</p>
        </DashboardCard>
        <DashboardCard title="Global Rankings">
          <p>Explore how movies rank globally across users.</p>
        </DashboardCard>
      </div>
    </div>
  );
}
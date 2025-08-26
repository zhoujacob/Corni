import { useAuth } from "../features/auth/AuthContext";
import DashboardCard from "../shared/DashboardCard";
import { ROUTES } from "../app/routes/path";
import { Link } from "react-router-dom";
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
        <Link to={ROUTES.RATE_MOVIES} className={styles.cleanLink}>
          <DashboardCard title="Rate Movies">
            <p>Rate movies you've watched!</p>
          </DashboardCard>
        </Link>
        <Link to={ROUTES.MY_MOVIES} className={styles.cleanLink}>
          <DashboardCard title="My Movies">
            <p>Review movies you've rated.</p>
          </DashboardCard>
        </Link>
        <DashboardCard title="Global Rankings">
          <p>Explore how movies rank globally across users.</p>
        </DashboardCard>
        {/* <DashboardCard title="My Groups">
          <p>View and manage your movie groups.</p>
        </DashboardCard> */}
      </div>
    </div>
  );
}
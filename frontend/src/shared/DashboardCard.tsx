import React from 'react';
import styles from './DashboardCard.module.css';

interface DashboardCardProps {
  title: string;
  onClick?: () => void;
  children?: React.ReactNode;
}

export default function DashboardCard({ title, onClick, children }: DashboardCardProps) {
  return (
    <div onClick={onClick} className={styles.card}>
      <h2 style={{ marginBottom: '0.5rem' }}>{title}</h2>
      <div>{children}</div>
    </div>
  );
}

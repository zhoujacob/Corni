import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import styles from './MyMoviesPage.module.css'
import { fetchUserMovies } from '../api/movieApi'
import type { Movie, UserMovie } from '../types/movie'
import { ROUTES } from '../app/routes/path'

// using shared types/UserMovie

export default function MyMoviesPage() {
  const navigate = useNavigate()
  const [items, setItems] = useState<UserMovie[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const PAGE_SIZE = 24
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE)

  useEffect(() => {
    let active = true
    setLoading(true)
    fetchUserMovies()
      .then((data) => {
        if (!active) return
        const arr = Array.isArray(data) ? data as UserMovie[] : []
        setItems(arr)
        setError(null)
      })
      .catch((err) => {
        console.error(err)
        if (!active) return
        setError('Failed to load your movies')
      })
      .finally(() => active && setLoading(false))
    return () => { active = false }
  }, [])

  const handleOpen = (m: Movie) => {
    navigate(ROUTES.MOVIE_DETAIL.replace(':tmdb_id', String(m.tmdb_id)))
  }

  if (loading) return <div className={styles.container}><p>Loading…</p></div>
  if (error) return <div className={styles.container}><p className={styles.error}>{error}</p></div>

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>My Top Movies</h1>
      {items.length === 0 ? (
        <p className={styles.empty}>You haven’t rated any movies yet.</p>
      ) : (
        <div className={styles.grid}>
          {items.slice(0, visibleCount).map(({ movie, rating }) => (
            <button key={movie.tmdb_id} className={styles.card} onClick={() => handleOpen(movie)}>
              {movie.poster_path ? (
                <img
                  className={styles.poster}
                  src={`https://image.tmdb.org/t/p/w300${movie.poster_path}`}
                  alt={movie.title}
                  loading="lazy"
                />
              ) : (
                <div className={styles.posterFallback}>{movie.title}</div>
              )}
              <div className={styles.meta}>
                <div className={styles.name}>{movie.title}</div>
                <div className={styles.sub}>
                  <span className={styles.badge}>Elo {Math.round(rating)}</span>
                  {movie.release_year ? <span className={styles.dot}>•</span> : null}
                  {movie.release_year ? <span>{movie.release_year}</span> : null}
                </div>
              </div>
            </button>
          ))}
        </div>
      )}
      {items.length > visibleCount && (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: 16 }}>
          <button className={styles.loadMore} onClick={() => setVisibleCount(c => c + PAGE_SIZE)}>
            Show more
          </button>
        </div>
      )}
    </div>
  )
}

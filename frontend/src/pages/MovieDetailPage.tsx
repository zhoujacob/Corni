import { useEffect, useState } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import type { Movie } from '../types/movie'
import { fetchMovieDetails } from '../api/movieApi'
import styles from './MovieDetailPage.module.css'

export default function MovieDetailPage() {
  const { tmdb_id } = useParams<{ tmdb_id: string }>()
  const location = useLocation()
  const navigate = useNavigate()

  const [movie, setMovie] = useState<Movie | null>(location.state?.movie || null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  console.log("Enter")
  
  useEffect(() => {
    if (!movie && tmdb_id) {
      setLoading(true)
      fetchMovieDetails(tmdb_id)
        .then(data => {
          setMovie(data)
          setError(null)
        })
        .catch(err => {
          console.error(err)
          setError('Failed to load movie details')
        })
        .finally(() => setLoading(false))
    }
  }, [movie, tmdb_id])

  const handleBack = () => navigate(-1)

  if (loading) return <div className={styles.container}><p>Loading…</p></div>
  if (error || !movie) return (
    <div className={styles.container}>
      <button className={styles.back} onClick={handleBack}>← Back</button>
      <p className={styles.error}>{error || 'Movie not found.'}</p>
    </div>
  )

  return (
    <div className={styles.container}>
      <button className={styles.back} onClick={handleBack}>← Back</button>
      <div className={styles.header}>
        <img
          className={styles.poster}
          src={`https://image.tmdb.org/t/p/w300${movie.poster_path}`}
          alt={movie.title}
        />
        <div className={styles.info}>
          <h1 className={styles.title}>{movie.title}</h1>
          <p className={styles.release}><strong>Release Date:</strong> {movie.release_year}</p>
        </div>
      </div>
      <div className={styles.overview}>
        <h2>Overview</h2>
        <p>{movie.overview}</p>
      </div>
    </div>
  )
}

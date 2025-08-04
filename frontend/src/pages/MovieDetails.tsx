import { useEffect, useState } from "react";
import styles from "./MovieDetails.module.css";

import { fetchMoviePreview } from "../api/movieApi"

let debounceTimer: ReturnType<typeof setTimeout>;
export default function MovieDetailsPage() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      setLoading(true)
      try {
        const response = await fetchMoviePreview(query);
        const movies = Array.isArray(response) ? response : [];
        setResults(movies);
         
      } catch {
        setResults([])
      } finally {
        setLoading(false)
      }
    }, 400)
  }, [query])

    return (
        <div className={styles.inputWrapper}>
            <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search for a movie..."
                className={styles.input}
                onKeyDown={e => e.key === "Enter"}
            />

            {loading && <p className={styles.loading}>Loading...</p>}

            {results.length > 0 && (
                <div className={styles.dropdown}>
                    {results.map((movie) => (
                    <div key={movie.tmdb_id} className={styles.movie}>
                        <h3 className={styles.movieTitle}>{movie.title}</h3>
                        <p className={styles.movieOverview}>{movie.release_date}</p>
                    </div>
                    ))}
                </div>
            )}
        </div>

    );
}

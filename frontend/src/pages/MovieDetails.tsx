import { useState } from "react";
import styles from "./MovieDetails.module.css";

import { fetchMoviePreview } from "../api/movieApi"

export default function MovieDetailsPage() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) return;
        setLoading(true);
        try {
            const res = await fetchMoviePreview(query);
            setResults(res.results || res);
        } catch (err) {
            console.error("Search failed", err);
        }
        setLoading(false);
    };

    return (
        <div className={styles.container}>
            <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search for a movie..."
                className={styles.input}
                onKeyDown={e => e.key === "Enter" && handleSearch()}
            />
            <button onClick={handleSearch} className={styles.button}>
                Search
            </button>

            {loading && <p>Loading...</p>}

            <div className={styles.results}>
                {results.map((movie, idx) => (
                <div key={idx} className={styles.movie}>
                    <h3 className={styles.movieTitle}>{movie.title}</h3>
                    <p className={styles.movieDate}>{movie.release_date}</p>
                    <p className={styles.movieOverview}>{movie.overview}</p>
                </div>
                ))}
            </div>
        </div>
    );
}

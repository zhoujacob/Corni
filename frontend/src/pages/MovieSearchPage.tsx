import { useState, useEffect, useRef } from 'react'
import type { KeyboardEvent } from 'react';
import { useNavigate } from 'react-router-dom'
import styles from "./MovieSearchPage.module.css";
import { ROUTES } from '../app/routes/path';
import PreviewMovie from "../features/movies/PreviewMovie";

import { fetchMoviePreview } from "../api/movieApi"
import type { Movie } from '../types/movie';

export default function MovieSearchPage() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    const inputRef = useRef<HTMLInputElement>(null)

    useEffect(() => {
        if (!query.trim()) {
        setResults([]);
        return;
        }

        const timer = setTimeout(async () => {
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
        }, 300)
        return () => clearTimeout(timer)
    }, [query])


    const onKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && results.length > 0) {
            handleSelect(results[0]);
        }
    }

    const handleSelect = (movie: Movie) => {
        console.log("Clicked movie:", movie);
        if (!movie?.tmdb_id) {
            console.error("Movie has no tmdb_id:", movie);
            return;
        }
        navigate(
            ROUTES.MOVIE_DETAIL.replace(':tmdb_id', movie.tmdb_id.toString())
        )
    };


    return (
        <div className={styles.inputWrapper}>
            <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search for a movie..."
                className={styles.input}
                onKeyDown={onKeyDown}
            />

            {loading && <p>Loading…</p>}

            {results.length > 0 && (
                <div className={styles.dropdown}>
                    {results.map((movie) => (
                        <PreviewMovie
                            key={movie.tmdb_id}
                            movie={movie}
                            onSelect={handleSelect}
                        />
                    ))}
                </div>
            )}
        </div>

    );
}

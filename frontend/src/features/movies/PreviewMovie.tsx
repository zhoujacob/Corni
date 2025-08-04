import type { KeyboardEvent } from 'react'
import styles from './PreviewMovie.module.css'
import type { Movie } from '../../types/movie';

interface PreviewMovieProps {
    movie: Movie
    onSelect: (movie: Movie) => void;
}

export default function PreviewMovie({ movie, onSelect }: PreviewMovieProps) {
    const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onSelect(movie);
        }
    };

    return (
        <div
            className={styles.option}
            onClick={() => onSelect(movie)}
            onKeyDown={handleKeyDown}
            tabIndex={0}
        >
            <h3 className="movie-title">{movie.title}</h3>
            <p className="movie-overview">{movie.release_year}</p>
        </div>
    );
}
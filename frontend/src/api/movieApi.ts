const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function fetchMoviePreview(query: string) {
    const res = await fetch(
        `${BASE_URL}/api/movies/preview/?q=${encodeURIComponent(query)}`
    );

    if (!res.ok)  {
        throw new Error('Failed to fetch movie preview');
    }
    return res.json();
}

export async function fetchMovieDetails(tmdb_id: string) {
    const res = await fetch(`${BASE_URL}/api/movies/${tmdb_id}/`);

    if (!res.ok) {
        throw new Error('Failed to fetch movie details');
    }
    return res.json();
}
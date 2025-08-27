const BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Ensure headers conform to the Fetch `HeadersInit` type
function authHeaders(): HeadersInit {
  try {
    const token = localStorage.getItem('accessToken');
    if (token) {
      return { Authorization: `Bearer ${token}` };
    }
    return {} as Record<string, string>;
  } catch {
    return {} as Record<string, string>;
  }
}

export async function fetchMoviePreview(query: string) {
    const res = await fetch(
        `${BASE_URL}/api/movies/preview/?q=${encodeURIComponent(query)}`,
        { headers: authHeaders() }
    );

    if (!res.ok)  {
        throw new Error('Failed to fetch movie preview');
    }
    return res.json();
}

export async function fetchMovieDetails(tmdb_id: string) {
    const res = await fetch(`${BASE_URL}/api/movies/${tmdb_id}/`, { headers: authHeaders() });

    if (!res.ok) {
        throw new Error('Failed to fetch movie details');
    }
    return res.json();
}

export async function fetchUserRatings() {
    const res = await fetch(`${BASE_URL}/api/movies/ratings/`, { headers: authHeaders() });

    if (!res.ok) {
        throw new Error('Failed to fetch user movies');
    }
    return res.json();
}

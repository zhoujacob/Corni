from tmdbv3api import TMDb, Movie as TMDbMovie
from .models import Movie as DjangoMovie
from django.conf import settings

tmdb = TMDb()
tmdb.api_key = settings.TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True

tmdb_movie = TMDbMovie()

def fetch_movies_from_tmdb(query: str):
    """
    Just fetch results from TMDb (no DB write)
    """
    return tmdb_movie.search(query)

def fetch_movie_by_id(tmdb_id: int):
    movie = tmdb_movie.details(tmdb_id)
    return movie
    
def serialize_tmdb_movie(movie_obj) -> dict:
    return {
        "title": getattr(movie_obj, "title", ""),
        "overview": getattr(movie_obj, "overview", ""),
        "poster_path": getattr(movie_obj, "poster_path", "") or "",
        "release_year": _normalize_release_year(getattr(movie_obj, "release_date", "")),
    }

def _normalize_release_year(release_date: str) -> int | None:
    try:
        return int(release_date.split("-")[0]) if release_date else None
    except Exception:
        return None
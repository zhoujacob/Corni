from tmdbv3api import TMDb, Movie as TMDbMovie
from .models import Movie as DjangoMovie
from django.conf import settings

tmdb = TMDb()
tmdb.api_key = settings.TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True

tmdb_movie = TMDbMovie()

def fetch_and_store_movies(query: str):
    results = tmdb_movie.search(query)
    
    for r in results:
        release_year = None 
        if getattr(r, "release_date", None):
            release_date = getattr(r, "release_date", None)
            if release_date:
                release_year = int(release_date.split("-")[0])

        DjangoMovie.objects.update_or_create(
            tmdb_id=getattr(r, "id"),
            defaults={
                "title": getattr(r, "title", ""),
                "overview": getattr(r, "overview", ""),
                "poster_path": getattr(r, "poster_path", ""),
                "release_year": release_year,
            }
        )


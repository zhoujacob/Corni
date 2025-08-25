from django.db import models
from django.conf import settings
from .constants import DEFAULT_ELO

# Create your models here.
class Movie(models.Model):
    title        = models.CharField(max_length=255)
    tmdb_id      = models.IntegerField(unique=True)
    overview     = models.TextField(blank=True)
    poster_path  = models.CharField(max_length=500, null = True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    last_synced  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MovieRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_ratings')
    rating = models.FloatField(default=DEFAULT_ELO)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
    
    def __str__(self):
        return f"{self.user} -> {self.movie.tmdb_id} ({self.movie.title}): {self.rating:.1f}"

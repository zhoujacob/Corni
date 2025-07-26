from django.db import models

# Create your models here.
class Movie(models.Model):
    title        = models.CharField(max_length=255)
    tmdb_id      = models.IntegerField(unique=True)
    overview     = models.CharField(max_length=255)
    poster_path  = models.CharField(max_length=500, null = True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    last_synced  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

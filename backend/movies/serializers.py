from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie 
        fields = ['id', 'title', 'tmdb_id', 'overview', 'poster_path', 'release_year', 'last_synced']

class MovieCompareSerializer(serializers.Serializer):
    movie1_id = serializers.IntegerField()
    movie2_id = serializers.IntegerField()
    winner_id = serializers.IntegerField()  # must equal movie1_id or movie2_id

class MovieLeaderboardItemSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField()
    num_ratings = serializers.IntegerField()
    bayes_rating = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ("id", "title", "tmdb_id", "avg_rating", "bayes_rating", "num_ratings")
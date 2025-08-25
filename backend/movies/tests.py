from typing import Any, cast
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from movies.models import Movie, MovieRating
from movies.constants import DEFAULT_ELO


class MovieCompareViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = cast(Any, User.objects).create_user(
            email="test@example.com", google_id="gid-1", first_name="Test", last_name="User"
        )
        self.client.force_authenticate(self.user)
        self.m1 = Movie.objects.create(title="Movie A", tmdb_id=101)
        self.m2 = Movie.objects.create(title="Movie B", tmdb_id=102)
        self.url = reverse("movie-compare")

    def test_updates_elo_for_user(self):
        payload = {"movie1_id": self.m1.tmdb_id, "movie2_id": self.m2.tmdb_id, "winner_id": self.m1.tmdb_id}
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        r1 = MovieRating.objects.get(user=self.user, movie=self.m1)
        r2 = MovieRating.objects.get(user=self.user, movie=self.m2)
        # Starting at 1500 vs 1500 with K=32, winner -> 1516, loser -> 1484
        self.assertAlmostEqual(r1.rating, 1516.0, places=1)
        self.assertAlmostEqual(r2.rating, 1484.0, places=1)

    def test_rejects_same_movie_ids(self):
        payload = {"movie1_id": self.m1.tmdb_id, "movie2_id": self.m1.tmdb_id, "winner_id": self.m1.tmdb_id}
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class MovieLeaderboardViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.u1 = cast(Any, User.objects).create_user(
            email="u1@example.com", google_id="gid-2", first_name="U1", last_name="User"
        )
        self.u2 = cast(Any, User.objects).create_user(
            email="u2@example.com", google_id="gid-3", first_name="U2", last_name="User"
        )
        self.a = Movie.objects.create(title="Alpha", tmdb_id=201)
        self.b = Movie.objects.create(title="Beta", tmdb_id=202)
        self.c = Movie.objects.create(title="Gamma", tmdb_id=203)

        # Ratings: A has 2 ratings (avg 1500), B has 1 rating, C has none
        MovieRating.objects.create(user=self.u1, movie=self.a, rating=1600)
        MovieRating.objects.create(user=self.u2, movie=self.a, rating=1400)
        MovieRating.objects.create(user=self.u1, movie=self.b, rating=1520)

        self.url = reverse("movie-leaderboard")

    def test_leaderboard_min_ratings_filter(self):
        resp = self.client.get(self.url + "?min_ratings=2")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # Only movie A should be present
        self.assertTrue(all(item["tmdb_id"] == self.a.tmdb_id for item in data))
        self.assertEqual(data[0]["num_ratings"], 2)
        self.assertAlmostEqual(data[0]["avg_rating"], 1500.0, places=1)

    def test_leaderboard_includes_expected_fields(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertGreaterEqual(len(data), 2)
        required_keys = {"id", "title", "tmdb_id", "avg_rating", "bayes_rating", "num_ratings"}
        self.assertTrue(required_keys.issubset(set(data[0].keys())))

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework import status

from users.models import CustomUser

class GoogleLoginTests(APITestCase):
    """
    Tests for the GoogleLoginView: new user, existing user, invalid token
    """

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('google-login')

    @patch('users.views.requests.get')
    def test_new_google_user(self, mock_get):
        # Simulate Google tokeninfo response for a new user
        mock_response = MagicMock(
            status_code=200,
            json=lambda: {
                "email": "roger@example.com",
                "sub": "ggwp",
                "given_name": "Roger",
                "family_name": "Chen"
            }
        )
        mock_get.return_value = mock_response

        response = self.client.post(self.url, {'token': 'dummy'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

        user = CustomUser.objects.get(email="roger@example.com")
        self.assertEqual(user.google_id, "ggwp")
        self.assertEqual(user.first_name, "Roger")
        self.assertEqual(user.last_name, "Chen")

    @patch('users.views.requests.get')
    def test_existing_google_user(self, mock_get):
        # Create an existing user with google_id already set
        user = CustomUser.objects.create_user( # type: ignore
            email="norman@example.com",
            google_id="ggwp123",
            first_name="Norman",
            last_name="Chen",
            password="pass"
        )
        mock_response = MagicMock(
            status_code=200,
            json=lambda: {
                "email": "norman@example.com",
                "sub": "ggwp123",
                "given_name": "Norman",
                "family_name": "Chen"
            }
        )
        mock_get.return_value = mock_response

        response = self.client.post(self.url, {'token': 'dummy'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

        # Ensure no duplicate user was created
        self.assertEqual(CustomUser.objects.filter(email="norman@example.com").count(), 1)

    @patch('users.views.requests.get')
    def test_invalid_token(self, mock_get):
        # Simulate a failed verification
        mock_response = MagicMock(status_code=400)
        mock_get.return_value = mock_response

        response = self.client.post(self.url, {'token': 'bad'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .serializers import UserSerializer


from users.models import CustomUser
from typing import cast

User = get_user_model()

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    # Expects a token from the front-end
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'no token'}, status=400)
        # verify with Google
        resp = requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
        )
        if resp.status_code != 200:
            return Response({'error': 'invalid token'}, status=400)
        
        data = resp.json()
        
        email = data['email']
        google_id = data.get("sub")
        first_name = data.get("given_name", "")
        last_name = data.get("family_name", "")

        if not email or not google_id:
            return Response({'error': 'Missing email or Google ID'}, status=400)

        user = cast(CustomUser, User.objects.get_or_create(email=email)[0])
    
        updated = False
        if not user.google_id:
            user.google_id = google_id 
            updated = True
        if not user.first_name:
            user.first_name = first_name
            updated = True
        if not user.last_name:
            user.last_name = last_name
            updated = True
        if updated:
            user.save()

        # JWT Token
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

class MeView(APIView):
    """
    Endpoint to return the currently‐authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data,
                        status=status.HTTP_200_OK)
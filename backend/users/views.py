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
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': token},
            timeout=5,
        )
        if resp.status_code != 200:
            return Response({'error': 'invalid token'}, status=400)
        
        data = resp.json()
        
        email = data['email']
        google_id = data.get("sub")
        first_name = data.get("given_name", "")
        last_name = data.get("family_name", "")
        aud = data.get("aud")

        if not email or not google_id:
            return Response({'error': 'Missing email or Google ID'}, status=400)

        # Best-effort audience validation when configured
        client_id = getattr(settings, 'GOOGLE_SSO_CLIENT_ID', None)
        if client_id and aud and aud != client_id:
            return Response({'error': 'Invalid audience'}, status=400)
        # Optionally ensure email is verified when present
        email_verified = data.get('email_verified')
        if email_verified in (False, 'false', 'False', '0'):
            return Response({'error': 'Email not verified'}, status=400)
        # Create or update user with defaults; ensure required fields provided
        user, created = cast(
            tuple[CustomUser, bool],
            User.objects.get_or_create(
                email=email,
                defaults={
                    'google_id': google_id,
                    'first_name': first_name,
                    'last_name': last_name,
                },
            ),
        )
        if created:
            # Google sign-in users should not have local passwords
            user.set_unusable_password()
            user.save(update_fields=["password"])
        else:
            updated = False
            if not user.google_id:
                user.google_id = google_id
                updated = True
            if not user.first_name and first_name:
                user.first_name = first_name
                updated = True
            if not user.last_name and last_name:
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
    

class DevLoginView(APIView):
    """
    Development-only endpoint to login as a test user only in local
    
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.DEBUG:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        email = request.data.get("email")
        if not email:
            return Response({"detail": "email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"first_name": "Dev", "last_name": "User"},
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])
        
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )

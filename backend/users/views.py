import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

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
        name  = data.get('name', '')

        user, _ = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': name}
        )

        # JWT Token
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
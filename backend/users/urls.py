from django.urls import path
from .views import GoogleLoginView, MeView


# ENDPOINT: POST http://localhost:8000/api/auth/....
urlpatterns = [
    # Body: { "token": "<Google id_token>" }
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('me/', MeView.as_view(), name='me')
]

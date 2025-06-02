from django.urls import path
from .views import GoogleLoginView

urlpatterns = [
    
    # ENDPOINT: POST http://localhost:8000/api/auth/google-login/
    # Body: { "token": "<Google id_token>" }
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
]

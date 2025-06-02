from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({"message": "Welcome to the API 🚀"})

urlpatterns = [
    path('', root_view),
    path('api/auth/', include('users.urls')),
    
]

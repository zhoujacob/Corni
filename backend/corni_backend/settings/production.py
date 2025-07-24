from .base import *

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [IsAuthenticated],
    'DEFAULT_AUTHENTICATION_CLASSES': [SessionAuthentication],
}

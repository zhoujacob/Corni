from .base import *

from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [AllowAny],
    'DEFAULT_AUTHENTICATION_CLASSES': [SessionAuthentication],
}

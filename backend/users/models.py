from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # add extra profile fields here if you want
    pass

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Need a custom user manager since we are defining our own user model.
    This manager:
        1. Creates users correctly
        2. Set essential fields
        3. Handle validation for the custom setup

    When the app calls CustomUser.objects.create_user(...) -> it calls CustomUserManager.create_user(..)
    """

    def create_user(self, email, google_id=None, first_name='', last_name='', password=None):
        """
        Google users will still be required to have google_id when signing in through OAuth
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            google_id=google_id,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_unusable_password()  # It is logging in with google so password can't be set
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, google_id=None, first_name='', last_name='', password=None):
        user = self.create_user(
            email=email,
            google_id=google_id,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    In Django, .objects is the default manager for a model
    --> objects registers CustomUserManager as the default manager
    --> Enables calls like CustomUser.bojects.create_user(...)
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['google_id', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.first_name} {self.last_name})"
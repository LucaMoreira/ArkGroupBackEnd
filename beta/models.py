from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not username:
            raise ValueError("The Username must be set")
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user  = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username         = models.CharField(verbose_name="username", max_length=30,unique=True, blank=False, null=False, primary_key=True)
    email            = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=False, null=False)
    sub_id           = models.CharField(verbose_name='subscription', max_length=200, unique=True, blank=True, null=True)
    status           = models.BooleanField(verbose_name='status', blank=False, null=False, unique=False, default=False)
    is_staff         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    date_joined      = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD   = 'username'
    REQUIRED_FIELDS  = ['email']
    
    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)
    
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class PasswordToken(models.Model):
    id         = models.CharField(verbose_name='id', max_length=200, unique=True, blank=False, null=False, primary_key=True)
    user       = models.CharField(verbose_name='user', max_length=30, unique=False, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.id
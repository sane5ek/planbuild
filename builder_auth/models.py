from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # add additional fields here
    username = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField('email address', unique=True, error_messages={'required': 'Пользователь с такой почтой уже существует.'})
    post = models.ForeignKey('builder.Post', null=True, default=None, on_delete=models.SET_DEFAULT)
    science_degree  = models.ForeignKey('builder.ScienceDegree', null=True, default=None, on_delete=models.SET_NULL)
    science_title = models.ForeignKey('builder.ScienceTitle', null=True, default=None, on_delete=models.SET_NULL)
    salary = models.FloatField(null=True, default=1)
    adopted_fields = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not first_name:
            raise ValueError('The First Name field must be set')
        if not last_name:
            raise ValueError('The Last Name field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.ADMINISTRATOR)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(
            first_name='Super', 
            last_name='User', 
            email=email, 
            password=password, 
            **extra_fields
        )

class User(AbstractUser):
    REGULAR_USER = 'regular_user'
    ADMINISTRATOR = 'admin'

    ROLE_CHOICES = [
        (REGULAR_USER, 'Regular User'),
        (ADMINISTRATOR, 'Admin')
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    profile = models.ImageField(upload_to='media/profile_pic/', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label =  'authentication'

    def __str__(self):
        return f"{self.first_name} {self.last_name} as ({self.role})"

class TrackFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'authentication'
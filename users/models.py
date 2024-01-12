from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True }


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    name = models.CharField(max_length=50, verbose_name='Name', **NULLABLE)
    lastname = models.CharField(max_length=50, verbose_name='Lastname', **NULLABLE)
    company = models.CharField(max_length=50, verbose_name='Company', **NULLABLE)

    avatar = models.ImageField(upload_to='users', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Phone number', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Country', **NULLABLE)

    birthday = models.DateField(verbose_name='Birthday', **NULLABLE)

    comment = models.CharField(max_length=300, verbose_name='Comment', **NULLABLE)
    is_manager = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

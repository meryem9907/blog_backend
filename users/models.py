from django.contrib.auth.models import AbstractUser
from django.db import models

class Author(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        unique=False
    )

    # default auth requirements were username and password, so here it is set to email and password
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email


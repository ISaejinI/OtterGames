from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    recompense = models.IntegerField(default=0)
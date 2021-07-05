from django.db import models

# Create your models here.
from django.db import models
# Create your models here.

class User(models.Model):
    user_phone = models.CharField("user_phone", max_length=12)
    secret_code = models.CharField("user_phone", max_length=6)

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

class Psychologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    @property
    def patient_id(self):
        return self.user.id
    
class PatientEvaluation:  # ce n'est pas un modèle de base de données, juste une classe normale
    def __init__(self, patient_id, text, emotion, confidence):
        self.patient_id = patient_id
        self.text = text
        self.emotion = emotion
        self.confidence = confidence

class Psychologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
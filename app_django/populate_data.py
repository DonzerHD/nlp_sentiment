import os
import random
import django

# Définir la variable d'environnement DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emotions_tracking.settings")

# Initialiser Django
django.setup()

# Importer les modèles et les documents Elasticsearch après l'initialisation de Django
from django.contrib.auth.models import User
from django.db import transaction
from accounts.models import Patient
from django_elasticsearch_dsl.registries import registry
from search.documents import PatientEvaluationDocument
from faker import Faker

# Créer une instance de Faker
fake = Faker()

# Définir les informations du patient
patient_info = {
    "username": "johnshhhmiththhfgfgestmmmfff",
    "password": "password123"
}

# Liste des émotions possibles
emotions = ["joy", "anger", "fear"]

# Insérer les données dans la base de données PostgreSQL
with transaction.atomic():
    user = User.objects.create_user(
        username=patient_info["username"],
        password=patient_info["password"]
    )
    patient = Patient.objects.create(user=user)

    # Générer les textes pour le patient
    for _ in range(5):
        text = fake.text()
        emotion = random.choice(emotions)
        confidence = random.uniform(0.0, 1.0)

        print(f"Boucle: {_}")
        # Insérer les données dans Elasticsearch
        document = PatientEvaluationDocument(
            meta={"id": None},
            text=text,
            emotion=emotion,
            confidence=confidence
        )
        document.save()
        
# Rafraîchir l'index Elasticsearch
PatientEvaluationDocument.init()

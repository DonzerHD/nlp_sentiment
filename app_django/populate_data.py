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
import uuid

# Rafraîchir l'index Elasticsearch
PatientEvaluationDocument.init()

# Créer une instance de Faker
fake = Faker()

# Liste des émotions possibles
emotions = ["joy", "anger", "fear"]

# Insérer les données dans la base de données PostgreSQL
with transaction.atomic():
    for i in range(3):  # Créer 3 utilisateurs
        user = User.objects.create_user(
            username=f"test_user_{i+5}",
            password="password123",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        patient = Patient.objects.create(user=user)
        
        for _ in range(5):  # Pour chaque utilisateur, générer 5 textes
            text = fake.text()
            emotion = random.choice(emotions)
            confidence = random.uniform(0.0, 1.0)
            document_id = uuid.uuid4()  
            document = PatientEvaluationDocument(
                meta={"id": document_id},
                patient_id=patient.id,  # Définissez l'ID du patient
                text=text,
                emotion=emotion,
                confidence=confidence
            )
            document.save()

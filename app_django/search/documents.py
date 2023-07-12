from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from accounts.models import Patient

@registry.register_document
class PatientEvaluationDocument(Document):
    id = fields.IntegerField(attr='id')
    text = fields.TextField(attr='text')
    emotion = fields.TextField(attr='emotion')
    confidence = fields.FloatField(attr='confidence')

    class Django:
        model = Patient  # le modèle Django est toujours nécessaire pour django_elasticsearch_dsl
        fields = []  # ne synchronise aucun champ avec le modèle Django

    class Index:
        name = 'patient_evaluations'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
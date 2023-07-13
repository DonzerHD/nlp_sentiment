from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from accounts.models import Patient , PatientEvaluation

@registry.register_document
class PatientEvaluationDocument(Document):
    id = fields.IntegerField(attr='id')
    patient_id = fields.IntegerField(attr='patient_id')  # Nouveau champ pour l'ID du patient
    text = fields.TextField(attr='text')
    emotion = fields.TextField(attr='emotion')
    confidence = fields.FloatField(attr='confidence')

    class Django:
        model = PatientEvaluation  # utilisez la nouvelle classe PatientEvaluation
        fields = []
    
    class Index:
        name = 'patient_evaluations'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}


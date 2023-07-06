#!/bin/bash

# Créer l'index avec le mapping
curl -X PUT "localhost:9200/notes" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "patient_lastname": { "type": "keyword" },
      "patient_firstname": { "type": "keyword" },
      "text": { "type": "text", "analyzer": "standard" },
      "date": { "type": "date" },
      "patient_left": { "type": "boolean" },
      "emotion": { "type": "keyword" },
      "confidence": { "type": "float" }
    }
  }
}
'


# patient_firstname : Le prénom du patient.
# patient_lastname : Le nom de famille du patient.
# date : La date de la note.
# text : Le texte de la note.
# emotion : L'émotion prédite par votre modèle de machine learning.
# confidence : La confiance de la prédiction de l'émotion.

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
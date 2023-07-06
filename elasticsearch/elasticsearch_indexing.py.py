import pickle
from elasticsearch import Elasticsearch
from faker import Faker
import string
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Charger le modèle pickle
with open('./model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Charger le vectorizer pickle
with open('./model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Chargement du modèle de langue Spacy
nlp = spacy.load('en_core_web_sm')

# Création de la liste des stopwords
stop_words = nlp.Defaults.stop_words
custom_stopwords = ['nt', 'm', 's', 't', 've', 'feel', 'feeling', 'feelings', 'like', 'know', 'want', 'time', 'think', 'little']
stop_words = stop_words.union(custom_stopwords)

# Fonction pour prétraiter le texte
def preprocess_text(text):
    text = text.lower()  # Convertir en minuscules
    text = text.translate(str.maketrans('', '', string.punctuation))  # Supprimer la ponctuation
    doc = nlp(text)
    text = " ".join([token.text for token in doc if not token.is_stop])  # Supprimer les stopwords
    return text

# Connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")
faker = Faker()

# Lire le fichier CSV
df = pd.read_csv('./data/Emotion_final.csv')

# Générer une liste de 400 patients fictifs
patient_list = []
for _ in range(400):
    patient_list.append((faker.first_name(), faker.last_name()))

# Itérer sur les lignes du DataFrame
for _, row in df.iterrows():
    # Sélectionner un patient de manière aléatoire dans la liste
    patient = faker.random.choice(patient_list)
    
    document = {
        "patient_firstname": patient[0],
        "patient_lastname": patient[1],
        "date": faker.date(),
        "text": row['Text']  # Utiliser le texte du fichier CSV
    }

    # Prétraitement du texte
    processed_text = preprocess_text(document['text'])

    # Extraction des features TF-IDF
    features = vectorizer.transform([processed_text])

    # Prédiction de l'émotion et de la confidence avec le modèle
    emotion = model.predict(features)[0]
    confidence = model.predict_proba(features)[0][model.classes_.tolist().index(emotion)]

    # Ajout des champs "emotion" et "confidence" au document
    document['emotion'] = emotion
    document['confidence'] = confidence

    # Indexation du document dans Elasticsearch
    es.index(index="notes", body=document)

print("Documents ajoutés avec succès.")

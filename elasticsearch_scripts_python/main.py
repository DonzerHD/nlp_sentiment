import pickle
from faker import Faker
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from preprocess import preprocess_text
from elasticsearch_script_python.utils import index_document

# Load the pickle model
with open('./model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the pickle vectorizer
with open('./model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

faker = Faker()

# Read the CSV file
df = pd.read_csv('./data/Emotion_final.csv')

# Generate a list of 400 fake patients
patient_list = []
for _ in range(400):
    patient_list.append((faker.first_name(), faker.last_name()))

# Iterate over the DataFrame rows
for _, row in df.iterrows():
    # Select a random patient from the list
    patient = faker.random.choice(patient_list)
    
    document = {
        "patient_firstname": patient[0],
        "patient_lastname": patient[1],
        "date": faker.date(),
        "text": row['Text']
    }

    # Preprocess the text
    processed_text = preprocess_text(document['text'])

    # Extract TF-IDF features
    features = vectorizer.transform([processed_text])

    # Predict the emotion and confidence using the model
    emotion = model.predict(features)[0]
    confidence = model.predict_proba(features)[0][model.classes_.tolist().index(emotion)]

    # Add the "emotion" and "confidence" fields to the document
    document['emotion'] = emotion
    document['confidence'] = confidence

    # Index the document in Elasticsearch
    index_document(document)

print("Documents added successfully.")
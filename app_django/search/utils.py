# utils.py
import requests

API_URL = "https://api-inference.huggingface.co/models/DonzerHD/text_class_emotion"
headers = {"Authorization": "Bearer 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"}

def evaluate_text(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    predictions = response.json()
    print(predictions)
    emotions = predictions[0]
    max_emotion = max(emotions, key=lambda x: x['score'])
    emotion = max_emotion['label']
    confidence = max_emotion['score']

    return emotion, confidence

import torch
from transformers import AutoModelForSequenceClassification

# Charger le modèle, le tokenizer, la configuration et emotion_to_int
checkpoint = torch.load("model_bon.pth", map_location=torch.device('cpu'))

# Charger la configuration
config = checkpoint["config"]

# Charger le modèle
model = AutoModelForSequenceClassification.from_config(config)
model.load_state_dict(checkpoint["model_state_dict"])

# Charger le tokenizer
tokenizer = checkpoint["tokenizer"]

# Charger emotion_to_int
emotion_to_int = checkpoint["emotion_to_int"]

# Créer une correspondance entre les indices et les labels
int_to_emotion = {i: emotion for emotion, i in emotion_to_int.items()}

# Phrase à prédire
text = "I am feeling very happy today!"

# Tokeniser la phrase
inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")

# Faire la prédiction
outputs = model(**inputs)

# Obtenir les scores de chaque classe
scores = outputs.logits

# Obtenir l'indice de la classe prédite
predicted_class_index = torch.argmax(scores).item()

# Obtenir le label de la classe prédite
predicted_class_label = int_to_emotion[predicted_class_index]

# Afficher le label de la classe prédite
print(predicted_class_label)

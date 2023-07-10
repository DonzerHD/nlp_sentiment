import pickle

# Charger le modèle à partir du fichier pickle
with open('model_final_django.pkl', 'rb') as file:
    model = pickle.load(file)



# # Exemple de texte à prédire
# text = "C'est un texte que vous voulez classifier"

# # Prétraitement du texte (si nécessaire)
# # ...

# # Effectuer la prédiction avec le modèle
# prediction = model.predict([text])

# # Afficher la prédiction
# print(prediction)
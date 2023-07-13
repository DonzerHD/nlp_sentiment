from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from elasticsearch_dsl import Search
from search.documents import PatientEvaluationDocument
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Patient
from search.forms import TextCreationForm
from search.utils import evaluate_text
from django.http import JsonResponse

class PatientEmotionsView(LoginRequiredMixin, View):
    template_name = 'search/emotions.html'
    login_url = '/login/'  # URL de la page de connexion

    def get(self, request):
        # Vérifier si l'utilisateur est un psychologue
        if not request.user.psychologist:
            # Rediriger vers la page d'accueil pour les patients
            return redirect('home')  # Remplacez 'home' par l'URL de la page d'accueil des patients

        # Obtenir le nom et le prénom de la requête
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')

        print(f"First name: {first_name}")
        print(f"Last name: {last_name}")

        # Chercher le patient par son nom et son prénom
        try:
            user = User.objects.get(first_name=first_name, last_name=last_name)
            patient_id = user.patient.id

            print(f"Patient ID: {patient_id}")

            # Créer une recherche Elasticsearch
            s = Search(index='patient_evaluations').filter('term', patient_id=patient_id)

            # Exécuter la recherche et obtenir les résultats
            response = s.execute()

            # Préparer la distribution des émotions
            emotion_distribution = {}
            for hit in response:
                if hit.emotion in emotion_distribution:
                    emotion_distribution[hit.emotion] += 1
                else:
                    emotion_distribution[hit.emotion] = 1

            print(f"Emotion distribution: {emotion_distribution}")

            return render(request, self.template_name, {'emotion_distribution': emotion_distribution})

        except User.DoesNotExist:
            print("User does not exist")

        return render(request, self.template_name, {'emotion_distribution': {}})

class TextSearchView(View):
    template_name = 'search/text_search.html'

    def get(self, request):
        if not request.user.is_superuser and not hasattr(request.user, 'psychologist'):
            return redirect('home')

        expression = request.GET.get('expression')

        s = Search(index='patient_evaluations')
        
        s = s.params(size=10000)

        if expression:
            s = s.query('match', text=expression)

        response = s.execute()

        results = []
        for hit in response:
            patient_id = hit.patient_id
            patient = Patient.objects.get(id=patient_id)
            results.append({
                'text': hit.text,
                'emotion': hit.emotion,
                'first_name': patient.user.first_name,
                'last_name': patient.user.last_name,
            })

        # Récupérer tous les résultats
        total_results = response.hits.total.value

        return render(request, self.template_name, {'results': results, 'total_results': total_results})
    
@login_required  # Pour s'assurer que seul un utilisateur connecté peut accéder à cette vue
def create_text(request):
    if request.method == 'POST':
        form = TextCreationForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            patient = request.user.patient
            emotion, confidence = evaluate_text(text)
            # Indexer le texte dans Elasticsearch
            patient_evaluation = PatientEvaluationDocument(
                patient_id=patient.id,
                text=text,
                emotion=emotion,
                confidence=confidence
            )
            patient_evaluation.save()
            
            return redirect('home')  # Rediriger vers la page d'accueil des patients
    else:
        form = TextCreationForm()
    
    return render(request, 'search/create_text.html', {'form': form})

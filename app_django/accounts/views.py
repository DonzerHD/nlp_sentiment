# views.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from .forms import PatientForm
from .models import Patient , Psychologist
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = '/'

    def get_success_url(self):
        return self.success_url
    
class CustomLogoutView(LogoutView):
    next_page = 'login'
    
class PatientCreateView(UserPassesTestMixin, CreateView):
    model = User
    form_class = PatientForm
    template_name = 'accounts/patient_form.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        Patient.objects.create(user=user, birth_date=form.cleaned_data["birth_date"])
        return super().form_valid(form)

    def test_func(self):
        return Psychologist.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        # Redirige vers la page de connexion si l'utilisateur n'est pas autorisé
        return redirect('login')
    
class PatientListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return Psychologist.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        # Redirige vers la page de connexion si l'utilisateur n'est pas autorisé
        return redirect('login')
    
    model = Patient
    template_name = 'accounts/patient_list.html'  # changez ceci pour correspondre à votre template
    context_object_name = 'patients'  # changez ceci pour le nom que vous voulez utiliser dans le template


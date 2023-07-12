from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class RestrictedAccessMixin(LoginRequiredMixin):
    login_url = 'login'  # URL de redirection en cas d'utilisateur non authentifié

class HomeView(RestrictedAccessMixin, TemplateView):
    template_name = 'home.html'
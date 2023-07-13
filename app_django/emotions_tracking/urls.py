"""emotions_tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views 
from emotions_tracking.views import HomeView
from search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('create_patient/', views.PatientCreateView.as_view(), name='create_patient'),
    path('patient_list/', views.PatientListView.as_view(), name='patient_list'),
    path('emotions/', search_views.PatientEmotionsView.as_view(), name='patient_emotions'),
    path('text-search/', search_views.TextSearchView.as_view(), name='text_search'),
    path('create-text/', search_views.create_text, name='create_text'),
]

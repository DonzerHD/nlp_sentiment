# forms.py
from django import forms

class TextCreationForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

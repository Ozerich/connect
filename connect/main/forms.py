from django import forms
from models import *
"""
class RegistrationForm(forms.Form):
    email = forms.EmailField()
    number = forms.CharField(max_length=7)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    
    def clean_number(self):
        try:
            User.objects.get(number=self.cleaned_data['number'])
        except:
            return self.cleaned_data['number']
            
    def save(self):
        return None
"""        

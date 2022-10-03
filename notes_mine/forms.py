from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile, Note, Category

# class RegistrationForm(forms.Form):
#   username = forms.CharField(max_length=100)
#   email = forms.EmailField()
#   password = forms.CharField(widget=forms.PasswordInput)
#   password2 = forms.CharField(widget=forms.PasswordInput)

#   # Vartotojo vardo validacija ir valymas:
#   def clean_username(self):
#     data = self.cleaned_data['username']
#     if User.objects.filter(username=data).exists():
#       raise ValidationError(_('Username %s is taken!') % data) 
#     return data

#   # Tikrinu el pasta:
#   def clean_email(self):
#     data = self.cleaned_data['email']
#     if User.objects.filter(email=data).exists():
#       raise ValidationError(_('Account with  email %s already exists!') % data)
#     return data

#   # Tikrinu du slaptazodziu laukus (visa lauku grupe):
#   def clean(self):
#     cleaned_data = super().clean()
#     password = cleaned_data['password']
#     password2 = cleaned_data['password2']
#     if password != password2:
#       raise ValidationError(_('Passwords do not match!'))
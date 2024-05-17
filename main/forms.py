from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from main.models import UserPengguna

class RegistFormPengguna(ModelForm):
    class Meta:
        model = UserPengguna
        fields = ('username', 'password', 'negara_asal',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'negara_asal': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Kata sandi harus terdiri dari minimal 8 karakter.")
        return password

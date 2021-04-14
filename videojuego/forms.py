from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profesor


class SignUp(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    genero = forms.ChoiceField(choices=[(1, 'Mujer'), (2, 'Hombre'), (3, 'Otro')])
    edad = forms.IntegerField(min_value=0)
    gradoEscolar = forms.IntegerField(min_value=1, max_value=9)

    class Meta:
        model = Profesor
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
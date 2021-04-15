from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Profesor


class SignUpProfessor(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    genero = forms.ChoiceField(choices=[(1, 'Mujer'), (2, 'Hombre'), (3, 'Otro')], label="Genero")
    edad = forms.IntegerField(min_value=0, label="Edad")
    gradoEscolar = forms.IntegerField(min_value=1, max_value=9, label="Grado Enseñanza")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            if fieldname in self.fields:
                self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'email', 'genero', 'edad', 'gradoEscolar')


class SignUpStudent(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    genero = forms.ChoiceField(choices=[(1, 'Mujer'), (2, 'Hombre'), (3, 'Otro')], label="Genero")
    edad = forms.IntegerField(min_value=0, label="Edad")
    gradoEscolar = forms.IntegerField(min_value=1, max_value=9, label="Grado Escolar")
    tokenProfesor = forms.CharField(max_length=10, min_length=10, label="Token del profesor")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

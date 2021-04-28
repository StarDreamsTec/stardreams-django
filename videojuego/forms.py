from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Profesor, Jugador, Genero, GradoEscolar, Sesion
import datetime

class SignUpProfessor(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    genero = forms.ChoiceField(choices=[(1, 'Mujer'), (2, 'Hombre'), (3, 'Otro')], label="Genero")
    edad = forms.IntegerField(min_value=0, label="Edad")
    gradoEscolar = forms.ChoiceField(choices=GradoEscolar.choices, label="Grado Escolar")

    def __init__(self, *args, **kwargs):
        super(SignUpProfessor, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirma contraseña"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        for fieldname in ['username', 'password1', 'password2']:
            if fieldname in self.fields:
                self.fields[fieldname].help_text = None

    def save(self):
        data = self.cleaned_data
        user = super(SignUpProfessor, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        professor = Profesor.objects.create(user=user, genero=data['genero'], edad=data['edad'],
                                            gradoEscolar=data['gradoEscolar'])
        return professor


class SignUpStudent(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    genero = forms.ChoiceField(choices=Genero.choices, label="Genero")
    edad = forms.IntegerField(min_value=0, label="Edad")
    gradoEscolar = forms.ChoiceField(choices=GradoEscolar.choices, label="Grado Escolar")
    tokenProfesor = forms.CharField(max_length=10, min_length=10, label="Token del profesor", required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Opcional'}))

    def __init__(self, *args, **kwargs):
        super(SignUpStudent, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirma contraseña"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self):
        data = self.cleaned_data
        user = super(SignUpStudent, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        student = Jugador.objects.create(user=user, genero=data['genero'], edad=data['edad'],
                                           gradoEscolar=data['gradoEscolar'], profesor=data['tokenProfesor'])
        Sesion.objects.create(inicio = datetime.datetime.now(), fin = datetime.datetime.now(), jugador = student)
        return student


class Login(forms.Form):
    username = forms.CharField(max_length=30, required=True, label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Contraseña')


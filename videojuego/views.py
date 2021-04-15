from django.core.serializers import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

def index(request):
    # return HttpResponse('<h1>Hola desde Django</h1>')
    return render(request, 'index.html')


def indicadores(request):
    return render(request, 'indicadores.html')


def signup(request):
    if "type" in request.COOKIES:
        type_user = int(request.COOKIES['type'])
        print(request.method)
        print(type_user)
        if request.method == 'POST':
            if type_user != 0:
                if type_user == 1:
                    form = SignUpStudent(request.POST)
                else:
                    form = SignUpProfessor(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                return render(request, 'signup.html', {'form': form})
        elif request.method == 'CUSTOM':
            if type_user != 0:
                if type_user == 1:
                    form = SignUpStudent()
                else:
                    form = SignUpProfessor()
                response = HttpResponse(form.as_table())
                return response
    return render(request, 'signup.html', {})


def login(request):
    return render(request, 'registration/login.html')


def register(request):
    return render(request, 'registration/register.html')

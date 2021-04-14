from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUp
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from json import loads
# from . models import Reto
import psycopg2
# Create your views here.

def index(request):
    # return HttpResponse('<h1>Hola desde Django</h1>')
    return render(request, 'index.html')


def indicadores(request):
    return render(request, 'indicadores.html')


def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUp()
    return render(request, 'signup.html', {'form': form})


def login(request):
	return render(request, 'registration/login.html')

def register(request):
	return render(request, 'registration/register.html')

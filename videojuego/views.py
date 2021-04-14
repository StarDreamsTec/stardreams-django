from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from json import loads
# from . models import Reto
import psycopg2
# Create your views here.

def index(request):
	#return HttpResponse('<h1>Hola desde Django</h1>')
	return render(request, 'index.html')

def indicadores(request):
	return render(request, 'indicadores.html')

def login(request):
	return render(request, 'registration/login.html')

def register(request):
	return render(request, 'registration/register.html')
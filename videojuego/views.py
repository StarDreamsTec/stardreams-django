from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	#return HttpResponse('<h1>Hola desde Django</h1>')
	return render(request, 'index.html')

def indicadores(request):
	return render(request, 'indicadores.html')
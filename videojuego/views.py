from django.core.serializers import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from json import loads;
from django.contrib import messages
import psycopg2
import datetime
from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/')
def indicadores(request):
    print(request.user)
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
                    django_user = user.user
                    auth_login(request, django_user)
                    return redirect('/indicadores/')
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
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request, username=data['username'], password=data['password'])
            print(data['username'])
            print(data['password'])
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect('/indicadores/')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('/login/')
    else:
        form=Login()
    return render(request, 'login.html', {'form':form})


def dashboard(request):
	return render(request, 'registration/dashboard.html')

@csrf_exempt
def login_unity(request):
    #body_unicode = request.body.decode('utf-8')
    #body_json = loads(body_unicode) #convertir de string a JSON
    #user_request = body_json['usuario']
    #resultados = Jugador.objects.filter(user__username = user_request)
    #resultados = User.objects.filter(username = user_request)
    #userID = resultados[0].user.index
    #retorno = {"userID":userID}
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request, username=data['username'], password=data['password'])
            print(data['username'])
            print(data['password'])
            print(user)
            if user is not None:
                resultado = User.objects.filter(username = data['username']).first()
                FN = resultado.first_name
                LN = resultado.last_name
                ID = resultado.id
                retorno = {"id": ID, "first_name": FN, "last_name":LN}
                return JsonResponse(retorno)
            else:
                retorno = {}
                return JsonResponse(retorno)
@csrf_exempt
def send_level_data_unity(request):
    body_unicode = request.body.decode('utf-8')
    body_json = loads(body_unicode) #convertir de string a JSON
    rama = body_json['rama']
    completado = body_json['completado']
    tiempo = body_json['tiempo']
    username = body_json['username']
    jugador = Jugador.objects.filter(user__username = username).first()
    resultado = Nivel(completado = completado, tiempo = tiempo, rama = rama, tiempoTerminacion = datetime.datetime.now(), jugador = jugador)
    resultado.save()
    retorno = {"completado" : True}
    return JsonResponse(retorno)

@csrf_exempt
def close_unity(request):
    if request.method == 'POST':
        userid = request.POST['userID']
        jugador = Jugador.objects.filter(user__id=userid).first()
        duracion = int(float(request.POST['duracion']))
        fecha = datetime.date.today()
        sesion = Sesion.objects.create(duracion=duracion, fecha=fecha, jugador=jugador)
        if sesion is not None:
            flag = True
        else:
            flag = False
        retorno = {'confirm': flag}
        return JsonResponse(retorno)

    


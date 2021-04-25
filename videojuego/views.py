from functools import reduce

from django.core.serializers import json
from django.db.models import Count, Avg, Min, Max, Sum, F
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from json import loads, dumps
from django.contrib import messages
import datetime
from .models import *
from itertools import groupby


# Create your views here.

def index(request):
    return render(request, 'index.html')


def levelData(rama):
    data = Nivel.objects.filter(completado=True, rama=rama)
    level = {
        'completo': data.order_by('jugador__id').distinct('jugador').count(),
        'avg_time': data.aggregate(avg=Avg('tiempo'))['avg'],
        'min': data.aggregate(mint=Min('tiempo'))['mint'],
        'max': data.aggregate(maxt=Max('tiempo'))['maxt'],
        'avg_success': round(data.count()/Nivel.objects.filter(rama=rama).count()*100, 2)
    }
    return level


def profAge(mi, ma):
    data = Profesor.objects.filter(edad__gte=mi, edad__lt=ma)
    return reduce(lambda acc, prof: acc + Jugador.objects.filter(profesor=prof.token).count(), data, 0)


@login_required(login_url='/login/')
def indicadores(request):
    # TOTAL PER MONTH
    totalMonth = Sesion.objects.filter(inicio__month=datetime.datetime.now().month).order_by('jugador_id').distinct(
        'jugador').count()

    # ALL TIME TOTAL
    total = Sesion.objects.order_by('jugador_id').distinct('jugador').count()

    # PLAYERS WHO COMPLETED
    completo_query = Nivel.objects.filter(completado=True).order_by('jugador__id', 'rama',
                                                                    'tiempoTerminacion').distinct('jugador', 'rama')
    completo_groups = groupby(completo_query, lambda x: x.jugador)
    completo_glen = [len(list(group[1])) for group in completo_groups]
    completo = reduce(lambda acc, y: acc + 1 if y == 4 else acc, completo_glen, 0)

    # PREFERRED BRANCH
    rama_query = Jugador.objects.values('ramaPreferida').annotate(count=Count('ramaPreferida')).filter(count__gte=1). \
        order_by('count').first()
    rama = Rama.choices[rama_query['ramaPreferida'] - 1][1]

    # ALL TIME MINUTES
    sesion_time = Sesion.objects.annotate(duration=F('fin') - F('inicio'))
    total_minutes = round(sesion_time.aggregate(sum=Sum('duration'))['sum'].total_seconds() / 60, 2)

    # AVG SESION
    avg_sesion = total_minutes / sesion_time.count()

    # MAXIMUM AND MINIMUM TIME
    comp_grouper = groupby(completo_query, lambda x: x.jugador)
    comp_list_groups = [list(group) for jugador, group in comp_grouper]
    comp_list_valid = filter(lambda x: len(x) == 4, comp_list_groups)
    finish_times = {group[0].jugador.user.get_full_name(): reduce(lambda acc, x: acc + x.tiempo, group, 0) for group in comp_list_valid}
    min_time = min(finish_times, key=finish_times.get)
    max_time = max(finish_times, key=finish_times.get)

    # GENDER GROUPS
    ninas = Jugador.objects.filter(genero=1).annotate(count=Count('genero')).count()
    ninos = Jugador.objects.filter(genero=2).annotate(count=Count('genero')).count()
    otros = Jugador.objects.filter(genero=3).annotate(count=Count('genero')).count()
    genero = [ninas, ninos, otros]

    # AGE GROUPS
    age_group = [[key, len(list(l))] for key, l in groupby(Jugador.objects.all().order_by('edad'), lambda x: x.edad)]
    for i in range(0, len(age_group)):
        age_group[i].append('#FF43C0' if i % 2 == 0 else '#3AFFFF')
    age_group.insert(0, ['Age', 'Cantidad', {'role': 'style'}])

    # PROFESSOR AND AGE
    prof = [profAge(20, 30), profAge(30, 40), profAge(40, 50), profAge(50, 60), profAge(60, 100)]

    # DIST PER AREA
    s = Jugador.objects.filter(ramaPreferida=Rama.CIENCIA).count()
    t = Jugador.objects.filter(ramaPreferida=Rama.TEC).count()
    e = Jugador.objects.filter(ramaPreferida=Rama.ING).count()
    m = Jugador.objects.filter(ramaPreferida=Rama.MAT).count()
    area = [s, t, e, m]

    # NIVELES
    ciencia = levelData(Rama.CIENCIA)
    tec = levelData(Rama.TEC)
    ing = levelData(Rama.ING)
    mat = levelData(Rama.MAT)

    context = {
        'month': totalMonth,
        'total': total,
        'minutes': total_minutes,
        'avg_sesion': avg_sesion,
        'min': {'name': min_time, 'time': finish_times[min_time]},
        'max': {'name': max_time, 'time': finish_times[max_time]},
        'completo': completo,
        'rama': rama,
        'genero': dumps(genero),
        'age': dumps(age_group),
        'prof': dumps(prof),
        'area': dumps(area),
        'ciencia': ciencia,
        'tec': tec,
        'ing': ing,
        'mat': mat,
    }

    return render(request, 'indicadores.html', context)


def signup(request):
    if "type" in request.COOKIES:
        type_user = int(request.COOKIES['type'])
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
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                auth_login(request, user)
                return redirect('/indicadores/')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('/login/')
    else:
        form = Login()
    return render(request, 'login.html', {'form': form})


def dashboard(request):
    return render(request, 'registration/dashboard.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


@csrf_exempt
def login_unity(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                resultado = User.objects.filter(username=data['username']).first()
                FN = resultado.first_name
                LN = resultado.last_name
                ID = resultado.id
                retorno = {"id": ID, "first_name": FN, "last_name": LN}  # id_sesion
                return JsonResponse(retorno)
            else:
                retorno = {}
                return JsonResponse(retorno)


@csrf_exempt
def send_level_data_unity(request):
    body_unicode = request.body.decode('utf-8')
    body_json = loads(body_unicode)  # convertir de string a JSON
    rama = body_json['rama']
    completado = body_json['completado']
    tiempo = body_json['tiempo']
    username = body_json['username']
    jugador = Jugador.objects.filter(user__username=username).first()
    resultado = Nivel(completado=completado, tiempo=tiempo, rama=rama, tiempoTerminacion=datetime.datetime.now(),
                      jugador=jugador)
    resultado.save()
    retorno = {"completado": True}
    return JsonResponse(retorno)


@csrf_exempt
def close_unity(request):
    if request.method == 'POST':
        userid = request.POST['userID']
        jugador = Jugador.objects.filter(user__id=userid).first()
        duracion = int(float(request.POST['duracion']))
        fecha = datetime.date.today()
        sesion = Sesion.objects.create(duracion=duracion, fecha=fecha, jugador=jugador)  # Crea un objeto sesión
        retorno = {'confirm': sesion is not None}
        return JsonResponse(retorno)

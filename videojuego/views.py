from functools import reduce
from django.db.models import Count, Avg, Min, Max, Sum, F
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from json import loads, dumps
from django.contrib import messages
from .models import *
from itertools import groupby
from datetime import timedelta

# Create your views here.

def index(request):
    return render(request, 'index.html')


def levelData(rama):
    data = Nivel.objects.filter(completado=True, rama=rama)
    level = {
        'completo': data.order_by('jugador__id').distinct('jugador').count(),
        'avg_time': round(data.aggregate(avg=Avg('tiempo'))['avg'], 2),
        'min': round(data.aggregate(mint=Min('tiempo'))['mint'], 2),
        'max': round(data.aggregate(maxt=Max('tiempo'))['maxt'], 2),
        'avg_success': round(data.count()/Nivel.objects.filter(rama=rama).count()*100, 2)
    }
    return level


def profAge(mi, ma):
    data = Profesor.objects.filter(edad__gte=mi, edad__lt=ma)
    return reduce(lambda acc, prof: acc + Jugador.objects.filter(profesor=prof.token).count(), data, 0)


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
    rama_query = Jugador.objects.exclude(ramaPreferida=Rama.NONE).values('ramaPreferida').annotate(count=Count('ramaPreferida')).filter(count__gte=1). \
        order_by('count').last()
    rama = Rama.choices[rama_query['ramaPreferida']][1]

    # ALL TIME MINUTES
    sesion_time = Sesion.objects.annotate(duration=F('fin') - F('inicio'))
    total_minutes = round(sesion_time.aggregate(sum=Sum('duration'))['sum'].total_seconds() / 60, 2)

    # AVG SESION
    avg_sesion = round(total_minutes / sesion_time.count(), 2)

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
        'min': {'name': min_time, 'time': round(finish_times[min_time], 2)},
        'max': {'name': max_time, 'time': round(finish_times[max_time], 2)},
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
                    return redirect('/dashboard/')
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
                return redirect('/dashboard/')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('/login/')
    else:
        form = Login()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login/')
def dashboardSelect(request):
    isPlayer = Jugador.objects.filter(user=request.user).exists()
    if isPlayer:
        return studentDashboard(request)
    else:
        return profDashboard(request)


@login_required(login_url='/login/')
def studentDashboard(request):
    jugador = Jugador.objects.get(user=request.user)
    ciencia_comp = Nivel.objects.filter(jugador=jugador, rama=Rama.CIENCIA, completado=True).exists()
    tec_comp = Nivel.objects.filter(jugador=jugador, rama=Rama.TEC, completado=True).exists()
    ing_comp = Nivel.objects.filter(jugador=jugador, rama=Rama.ING, completado=True).exists()
    mat_comp = Nivel.objects.filter(jugador=jugador, rama=Rama.MAT, completado=True).exists()
    prof_query = Profesor.objects.filter(token=jugador.profesor)
    prof = prof_query.first().user.get_full_name() if prof_query.exists() else "No asignado"
    sesion_query = Sesion.objects.filter(jugador=jugador)
    if sesion_query.exists():
        sesion_time = Sesion.objects.filter(jugador=jugador).annotate(duracion=F('fin') - F('inicio'))
        min_full = round(sesion_time.aggregate(sum=Sum('duracion'))['sum'].total_seconds() / 60, 2)
        avg_sesion =  round(sesion_time.aggregate(avg=Avg('duracion'))['avg'].total_seconds() / 60, 2)
    else:
        min_full = 0
        avg_sesion = 0
    sesions= Sesion.objects.filter(jugador=jugador).order_by('-inicio').values('inicio', 'fin')[:10]
    context = {
        'rama': jugador.get_ramaPreferida_display(),
        'personaje_astro': jugador.personaje == Personaje.ASTRO,
        'coral': ciencia_comp,
        'astro': tec_comp,
        'castillo': ing_comp,
        'tort': mat_comp,
        'genero': jugador.get_genero_display(),
        'edad': jugador.edad,
        'grado': jugador.get_gradoEscolar_display(),
        'prof': prof,
        'min_tot': min_full,
        'avg_sesion':avg_sesion,
        'sesions': sesions,
        'intentos': {
            'ciencia': Nivel.objects.filter(jugador=jugador, rama=Rama.CIENCIA).count(),
            'tec': Nivel.objects.filter(jugador=jugador, rama=Rama.TEC).count(),
            'ing': Nivel.objects.filter(jugador=jugador, rama=Rama.ING).count(),
            'mat': Nivel.objects.filter(jugador=jugador, rama=Rama.MAT).count(),
        }
    }
    return render(request, "dashboard.html", context=context)


def profDashboard(request):
    profesor = Profesor.objects.get(user=request.user)
    estudiantes = Jugador.objects.filter(profesor=profesor.token)
    context = {
        'genero': profesor.get_genero_display(),
        'edad': profesor.edad,
        'grado': profesor.get_gradoEscolar_display(),
        'token': profesor.token,
        'students': estudiantes
    }
    return render(request, "prof_dashboard.html", context)


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
                ID = resultado.id
                if Jugador.objects.filter(user=user).exists():
                    jugador = Jugador.objects.get(user=user)
                    sesion= Sesion.objects.create(inicio=datetime.datetime.now(), jugador=jugador)
                    SesionID = sesion.id
                    completado = jugador.is_complete()
                    ciencia = Nivel.objects.filter(rama=Rama.CIENCIA, jugador=jugador, completado=True).exists()
                    tec = Nivel.objects.filter(rama=Rama.TEC, jugador=jugador, completado=True).exists()
                    ing = Nivel.objects.filter(rama=Rama.ING, jugador=jugador, completado=True).exists()
                    mat = Nivel.objects.filter(rama=Rama.MAT, jugador=jugador, completado=True).exists()
                    profesor = False
                else:
                    SesionID = 0
                    completado = False
                    profesor = True
                    ciencia, tec, ing, mat = False, False, False, False
                retorno = {
                    "id": ID,
                    "first_name": FN,
                    'sesionID': SesionID,
                    'ciencia': ciencia,
                    'tec': tec,
                    'ing': ing,
                    'mat': mat,
                    'profesor': profesor
                }
                return JsonResponse(retorno)
            else:
                retorno = {}
                return JsonResponse(retorno)


@csrf_exempt
def level_unity(request):
    body_unicode = request.body.decode('utf-8')
    body_json = loads(body_unicode)  # convertir de string a JSON
    rama = body_json['rama']
    completado = body_json['completado']
    tiempo = body_json['tiempo'] # duracion
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
        char = request.POST['characterID']
        sesion = request.POST['sesionID']
        jugador = Jugador.objects.get(user__id=userid)
        jugador.personaje = char
        jugador.save()
        sesion_obj = Sesion.objects.get(id=sesion)
        sesion_obj.fin = datetime.datetime.now()
        sesion_obj.save()
        retorno = {'confirm': sesion is not None}
        return JsonResponse(retorno)

@csrf_exempt
def ramaSteam(request):
    if request.method == 'POST':
        userid = request.POST['userID']
        ramaid = request.POST['ramaID']
        jugador = Jugador.objects.get(user__id=userid)
        jugador.ramaPreferida = int(ramaid)
        jugador.save()
        retorno = {'confirm' : True}
        return JsonResponse(retorno)

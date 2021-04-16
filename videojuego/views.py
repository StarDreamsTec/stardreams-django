from django.core.serializers import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
import json
from django.contrib import messages

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


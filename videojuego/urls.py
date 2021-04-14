from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('indicadores/', views.indicadores, name='indicadores'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    
    # path('proceso', views.proceso, name = 'proceso'),
    # path('datos',views.datos, name = 'datos'),
]

#urlpatterns += [
 #   path('accounts/', include('django.contrib.auth.urls')),
#]

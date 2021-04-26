from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('indicadores/', views.indicadores, name='indicadores'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard/', views.dashboardSelect, name='dashboard'),
    path('login_unity', views.login_unity, name='login_unity'),
    path('level_unity', views.level_unity, name='level_unity'),
    path('close_unity', views.close_unity, name='close_unity'),
    path('prof', views.profDashboard, name='prof'),
    path('ramaSteam', views.ramaSteam, name = 'ramaSteam'),
]

#urlpatterns += [
 #   path('accounts/', include('django.contrib.auth.urls')),
#]

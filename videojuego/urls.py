from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('indicadores/', views.indicadores, name='indicadores'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login_unity', views.login_unity, name='login_unity'),
    path('send_level_data_unity', views.send_level_data_unity, name='send_level_data_unity'),
    path('close_unity', views.close_unity, name='close_unity'),
    path('graficas/', views.graficas, name='graficas'),
    path('barras/', views.barras, name='barras'),
    
]

#urlpatterns += [
 #   path('accounts/', include('django.contrib.auth.urls')),
#]

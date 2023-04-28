from django.urls import path
from . import views


urlpatterns = [
    path('', views.home), 
    path('staff/', views.staff), 
    path('login/', views.login), 
    path('adminhome/', views.adhome),
    path('addfinger/', views.addfinger),
    path('crdata/', views.crdata),
    path('predict/', views.predicts),
    path('logout/', views.logout),
    path('vein/', views.vein),
    path('veinok/', views.veinok),
]

from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('',views.index, name="home"),
    path('service/',views.service, name="services"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/',views.logoutUser, name="logout"),
    
]

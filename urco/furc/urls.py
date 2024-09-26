from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('signupPage/', views.signupPage, name="signupPage"),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('login/', views.logIn, name='logIn'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('signup/', views.signUp, name='signUp')
]
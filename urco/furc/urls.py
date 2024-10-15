from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('signupPage/', views.signupPage, name="signupPage"),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('login/', views.logIn, name='logIn'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('signup/', views.signUp, name='signUp'),
    path('logout/', views.loggedOut, name='loggedOut'),
    path('researchStaff/', views.researchStaff, name='researchStaff'),
    path('supervisor/', views.supervisor, name='supervisor'),
    path('highApprover/', views.highApprover, name='highApprover'),
    path('new_order/', views.newOrder, name='newOrder'),
    path('current_order/', views.currentOrder, name='currentOrder'),
    path('previous_order/', views.previousOrder, name='previousOrder'),
    path('addOrder/', views.addOrder, name='addOrder'),
    path('orderStatusUpdate/', views.orderStatusUpdate, name='orderStatusUpdate'),
    path('orderView/<str:order_id>', views.orderView, name='orderView'),
    path('orderManager/', views.orderManager, name='orderManager'),
    path('stockManager/', views.stockManager, name='stockManager'),
    path('stockUpdate/', views.stockUpdate, name='stockUpdate')
    # path('s_pending_order/', views.superPendingOrder, name='superPendingOrder'),
    # path('addOrder/', views.addOrder, name='addOrder'),
    # path('addOrder/', views.addOrder, name='addOrder'),
]
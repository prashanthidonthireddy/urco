from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import User, UserRole


def index(request):
    return render(request, 'furc/loginPage.html')

def loginPage(request):
    return render(request, 'furc/loginPage.html')

def signupPage(request):
    return render(request, 'furc/signupPage.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpassword']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, 'You are successfully logged in')
            return redirect('/')

        else:
            messages.info(request, 'Invalid credential')
            return redirect('loginPage')

    else:
        return HttpResponse('404-PAGE NOT FOUND')

def forgotPassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['pass1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            messages.info(request, 'You are successfully logged in')
            return redirect('/')

        else:
            messages.info(request, 'Invalid credential')
            return redirect('loginPage')

    else:
        return HttpResponse('404-PAGE NOT FOUND')


def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        userRole = request.POST['userRole']
        print(userRole)
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        role = UserRole.objects.get(role_id=userRole)
        SpecialSym = ['$', '@', '#', '%']

        if password1!=password2:
            messages.info(request, 'Password1 and Password2 are different')
            return redirect('signUpPage')

        elif User.objects.filter(username=username).exists():
            messages.info(request, 'This username already exist')
            return redirect('signUpPage')
        elif len(password1)<8 and len(password1>20):
            messages.info(request, 'length of password would be between 8 to 20')
            return redirect('signUpPage')
        elif not any(char.isdigit() for char in password1):
            messages.info(request, 'Password should have at least one numeral')
            return redirect('signUpPage')
        elif not any(char.isupper() for char in password1):
            messages.info(request, 'Password should have at least one uppercase letter')
            return redirect('signUpPage')
        elif not any(char.islower() for char in password1):
            messages.info(request, 'Password should have at least one lowercase letter')
            return redirect('signUpPage')
        elif not any(char in SpecialSym for char in password1):
            messages.info(request, 'Password should have at least one of the symbols $@#')
            return redirect('signUpPage')
        else:
            users = User.objects.create_user(username=username, password=password1, role=role)
            users.save()
            messages.info(request, 'Your URCO account is successfully created')
            return redirect('/')
    else:
        return HttpResponse('404-page NOT FOUND')


from lib2to3.fixes.fix_input import context

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, request
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .models import User, UserRole, Chemical, Order, OrderItem, Laboratory


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
            role = user.role
            messages.info(request, 'You are successfully logged in')
            if str(role)=="Research Staff Member":
                print(role)
                return redirect('researchStaff')
            if str(role)=='Supervisor':
                return redirect('supervisor')
            if str(role)=='Higher Approver':
                return redirect('highApprover')
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

def loggedOut(request):
    logout(request)
    messages.info(request, "successfully loggedout")
    return redirect('/')

def researchStaff(request):
    return render(request, 'furc/researchStaff.html/')

def supervisor(request):
    return render(request, 'furc/researchStaff.html/')

def highApprover(request):
    return None

def newOrder(request):
    return render(request, 'furc/newOrder.html')

def currentOrder(request):
    current_order = Order.objects.filter(order_status='Pending approval')
    params = {'orders':current_order}
    return render(request, 'furc/current_order.html', params)

def previousOrder(request):
    previous_order = Order.objects.filter(order_status='Approved by supervisor')
    print(previous_order)
    params = {'orders': previous_order}
    return render(request, 'furc/previous_order.html', params)

def addOrder(request):
    if request.method == "POST":
        order_id=''
        if Order.objects.latest('order_id'):
            last_order = Order.objects.latest('order_id')
            last_order_id = last_order.order_id
            front_order_id = last_order_id[:1]
            back_order_id = last_order_id[1:]
            new_inc_id = int(back_order_id) +1
            order_id =  f"{front_order_id}{str(new_inc_id).zfill(len(back_order_id))}"
        else:
            order_id = 'E00001'
        print(order_id)
        lab_id = request.POST.get('lab')
        lab = Laboratory.objects.get(lab_id=lab_id)
        exp_name = request.POST.get('expName')
        exp_procedure = request.FILES.get('expProcedure')
        risk_assessment = request.FILES.get('riskAssessment')
        order_status = 'Pending approval'
        order = Order(order_id=order_id, exp_name=exp_name, lab_id=lab, exp_procedure=exp_procedure, risk_assessment=risk_assessment, order_status=order_status)
        order.save()

        chemicals_json = request.POST.get('chemicals')
        chemicals= json.loads(chemicals_json)

        for chemical in chemicals:
            chemical_name = chemical.get('chemicalName')
            get_chemical = Chemical.objects.get(chemical_id=chemical_name)
            quantity = chemical.get('quantity')
            print(type(get_chemical.uom))
            order_item = OrderItem(order_id=order, chemical_id=get_chemical, required_amount=quantity,uom=get_chemical.uom)
            order_item.save()
        messages.info(request, 'Your order has been sent for approval.')
        return redirect('currentOrder')
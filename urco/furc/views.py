from datetime import timezone, datetime
from lib2to3.fixes.fix_input import context

import dateutil.utils
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, request
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .models import User, UserRole, Chemical, Order, OrderItem, Laboratory, StockItem, StorageLocation


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
            if str(role)=='Order Manager':
                return redirect('orderManager')
            if str(role)=='Stock Manager':
                return redirect('stockManager')
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
    context={'order_status':'Closed', 'order_status':'Rejected by higher', 'order_status':'Rejected by supervisor'}
    current_order = Order.objects.all().exclude(order_status='Closed').exclude(order_status='Rejected by supervisor').exclude(order_status='Rejected by higher').order_by('-order_date')[0:3]
    previous_order = Order.objects.filter(**context).order_by('-order_date')[0:3]
    params={'current_order':current_order, 'previous_order': previous_order}
    return render(request, 'furc/researchStaff.html/', params)

def supervisor(request):
    top_pending_order = Order.objects.filter(order_status='Pending approval').order_by('-order_date')[0:3]
    top_approved_order = Order.objects.filter(order_status='Approved by supervisor').order_by('-order_date')[0:3]
    top_rejected_order = Order.objects.filter(order_status='Rejected by supervisor').order_by('-order_date')[0:3]
    top_escalated_order = Order.objects.filter(order_status='Pending higher approval').order_by('-order_date')[0:3]
    pending_order = Order.objects.filter(order_status='Pending approval')
    approved_order = Order.objects.filter(order_status='Approved by supervisor')
    rejected_order = Order.objects.filter(order_status='Rejected by supervisor')
    escalated_order = Order.objects.filter(order_status='Pending higher approval')
    params = {'pending_order':pending_order, 'approved_order':approved_order, 'rejected_order':rejected_order, 'escalated_order':escalated_order, 'top_pending_order':top_pending_order, 'top_approved_order': top_approved_order, 'top_rejected_order': top_rejected_order, 'top_escalated_order': top_escalated_order}
    return render(request, 'furc/supervisor.html/', params)

def highApprover(request):
    top_pending_order = Order.objects.filter(order_status='Pending higher approval').order_by('-order_date')[0:3]
    top_approved_order = Order.objects.filter(order_status='Approved by higher').order_by('-order_date')[0:3]
    top_rejected_order = Order.objects.filter(order_status='Rejected by higher').order_by('-order_date')[0:3]
    pending_order = Order.objects.filter(order_status='Pending higher approval')
    approved_order = Order.objects.filter(order_status='Approved by higher')
    rejected_order = Order.objects.filter(order_status='Rejected by higher')
    params = {'pending_order':pending_order, 'approved_order':approved_order, 'rejected_order':rejected_order, 'top_pending_order':top_pending_order, 'top_approved_order':top_approved_order, 'top_rejected_order':top_rejected_order }
    return render(request, 'furc/higherApprover.html/', params)

def orderManager(request):
    recent_orders = Order.objects.filter(order_status='Approved by higher')
    params = {'recent_orders': recent_orders}
    return render(request, 'furc/orderManager.html', params)

def stockManager(request):
    return render(request, 'furc/stockManager.html')
def newOrder(request):
    return render(request, 'furc/newOrder.html')

def currentOrder(request):
    current_order = Order.objects.all().exclude(order_status='Closed').exclude(order_status='Rejected by supervisor').exclude(order_status='Rejected by higher').order_by('-order_date')
    params = {'orders':current_order}
    return render(request, 'furc/current_order.html', params)

def previousOrder(request):
    context={'order_status':'Closed', 'order_status':'Rejected by higher', 'order_status':'Rejected by supervisor'}
    # previous_order = Order.objects.filter(order_status='Closed')
    previous_order = Order.objects.filter(**context)
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

def orderStatusUpdate(request):
    user = request.user
    if request.method == 'POST':
        if user.role.user_role=='Supervisor':
            order_id = request.POST['order_id']
            update = request.POST['status']
            order = Order.objects.get(order_id = order_id)
            if update=='Approve':
                messages.info(request, ' Order is approved')
                order.order_status='Approved by supervisor'
            elif update=='Reject':
                messages.info(request, ' Order is rejected')
                order.order_status='Rejected by supervisor'
            elif update=='Escalate':
                messages.info(request, ' Order is sent for higher approval')
                order.order_status='Pending higher approval'
            order.updated_date = dateutil.utils.today()
            order.save()
            return redirect('supervisor')
        elif user.role.user_role=='Higher Approver':
            order_id = request.POST['order_id']
            update = request.POST['status']
            order = Order.objects.get(order_id=order_id)
            if update == 'Approve':
                messages.info(request, ' Order is approved')
                order.order_status = 'Approved by higher'
            elif update == 'Reject':
                messages.info(request, ' Order is rejected')
                order.order_status = 'Rejected by higher'
            order.updated_date = dateutil.utils.today()
            order.save()
            return redirect('highApprover')
    return HttpResponse('404-Error')

def orderView(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order_item = OrderItem.objects.filter(order_id=order)
    order_items = []
    lab_stock=[]
    for i in order_item:
        quantity=0
        order_items.append(i)
        chemical_id = i.chemical_id
        lab_content_type = ContentType.objects.get_for_model(Laboratory)
        storage = StorageLocation.objects.filter(content_type=lab_content_type, location_id=order.lab_id.lab_id).first()
        labs = StockItem.objects.filter(storage_location=storage, chemical_id=chemical_id)
        for l in labs:
            quantity+=l.Current_stock
        lab_stock.append(quantity)
        sort_labs = StockItem.objects.filter(storage_location=storage, chemical_id=chemical_id).order_by('stock_id')
    is_order_manager = request.user.role.role_id == 5
    params = {'order': order, 'order_items': order_items,'is_order_manager': is_order_manager, 'lab_stock': lab_stock}
    return render(request, 'furc/order_det.html', params)

def stockUpdate(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        update = request.POST['status']
        order = Order.objects.get(order_id=order_id)
        if update=='Approve':
            order_item = OrderItem.objects.filter(order_id=order)
            for i in order_item:
                chemical_id = i.chemical_id
                amount = i.required_amount
                lab_content_type = ContentType.objects.get_for_model(Laboratory)
                storage = StorageLocation.objects.filter(content_type=lab_content_type, location_id=order.lab_id.lab_id).first()
                labs = StockItem.objects.filter(storage_location=storage, chemical_id=chemical_id)
                for l in labs:
                    if amount<=l.Current_stock:
                        l.Current_stock-=amount
                        break
                    amount-=l.Current_stock

            messages.info(request, ' Order is confirmed')
            order.order_status = 'Ordered'
            order.save()
            return redirect('orderManager')
        else:
            messages.info(request, ' Order is rejected')
            order.order_status = 'Rejected'
            order.save()
            return redirect('orderManager')

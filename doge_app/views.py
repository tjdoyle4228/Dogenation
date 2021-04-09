from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *
from django.db.models import Count 
from django import template
# Create your views here.
def index(request):
    return render(request,'index.html')

def create_user(request):
    if request.method =='POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/main_page')
    return redirect('/')

def main_page(request):
    if 'user_id' not in request.session:
        return redirect('/')    
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),

    }
    return render(request,"main_page.html",context)

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):
    if request.method == 'POST':
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/main_page')
        messages.error(request,"Email or password is wrong")
    return redirect('/login/page')

def login_page(request):
    return render(request,'login.html')

def add_dog(request):
    if request.method =='POST':
        errors = Dog.objects.create_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            dog = Dog.objects.create(name=request.POST['name'],breed=request.POST['breed'],age=request.POST['age'],gender=request.POST['gender'],owner=User.objects.get(id=request.session['user_id']))
            request.session['user_id'] = user.id
            return redirect('/main_page')
    return redirect('/')
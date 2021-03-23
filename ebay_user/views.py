from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import register_form, login_form
from .models import User

# Create your views here.
def login_user(request):
    if request.method == "GET":
        return render(request, 'ebay_user/login.html', {'form': login_form()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse('Successful login')
        return HttpResponse('Login Failed')

def logout_user(request):
    logout(request)
    return HttpResponse('This is a logout page')

def register_user(request):
    if request.method == 'GET':
        return render(request, 'ebay_user/register.html', {'form': register_form()})
    elif request.method == 'POST':
        submitted_form = register_form(request.POST)
        if submitted_form.is_valid():
            username = submitted_form.cleaned_data['username']
            password = submitted_form.cleaned_data['password1']

            # Register User
            my_user = User.objects.create_user(username=username, password=password)
            return HttpResponse('Successful registration')
        else:
            return HttpResponse("Form was filled incorrcectly")


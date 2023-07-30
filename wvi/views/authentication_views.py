from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from wvi.models import *


class CustomAuthentication():
    def loginView(request):
        if request.user.is_authenticated:
            return redirect('child')
        if request.method == "POST":
            username_login = request.POST['username']
            password_login = request.POST['password']
            user = authenticate(request, username=username_login, password=password_login)
            if user is not None:
                login(request, user)
                return redirect('child')
            else:
                msg = 'Error login'
                form = AuthenticationForm(request.POST)
                return render(request, 'login.html', {'form': form, 'msg': msg})
        else:
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form})
        
    def logoutView(request):
        if request.method == "GET":
            if request.user.is_authenticated:
                logout(request)
        return redirect('login')
    
    def signupView(request):
        if request.user.is_authenticated:
            return redirect('child')
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password1 = form.cleaned_data['password1']
                hashed_password = make_password(password1)
                user = form.save(commit=False)
                user.password = hashed_password
                user.save()
                user = authenticate(username=username, password=password1)
                login(request, user)
                return redirect('child')
            else:
                msg = 'Error Signup'
                return render(request, 'signup.html', {'form': form, 'msg': msg})
        else:
            form = UserCreationForm()
            return render(request, 'signup.html', {'form': form})
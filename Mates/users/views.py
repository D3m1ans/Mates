from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.template.context_processors import request
from django.urls import reverse
from .forms import CustomAutForm, CustomUserCreationForm

# Create your views here.

def main(request):
    return render(request, 'users/main.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html',{'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAutForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('main'))

    else:
        form = CustomAutForm()

    return render(request, 'users/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('main')
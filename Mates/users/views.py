from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.template.context_processors import request
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import CustomAutForm, CustomUserCreationForm, EditProfileForm


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

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})

@login_required
@require_http_methods(["GET", "POST"])
def edit_profile_view(request):
    user = request.user  # Получаем текущего пользователя

    if request.method == 'POST' and request.POST.get('_method') == 'PATCH':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = EditProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})
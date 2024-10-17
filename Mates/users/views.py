from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomAutForm

# Create your views here.

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAutForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse(''))

    else:
        form = CustomAutForm()

    return render(request, 'users/login.html', {'form': form})
from django.shortcuts import render, get_object_or_404
from .models import UserLibrary

# Create your views here.

def library_view(request):
    library = UserLibrary.objects.filter(user=request.user)
    return render(request, 'library/library.html', {'library': library})

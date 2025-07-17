from django.shortcuts import render, get_object_or_404
from .models import CustomUser


def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    context = {'user': user}
    return render(request, 'users/profile.html', context)

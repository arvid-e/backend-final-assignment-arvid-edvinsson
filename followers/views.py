from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import CustomUser
from .models import Follow


@login_required
def follow_user(request, username):
    return redirect('home')


@login_required
def unfollow_user(request, username):
    return redirect('home')
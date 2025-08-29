from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def follow_user(request, username):
    return redirect("home")


@login_required
def unfollow_user(request, username):
    return redirect("home")

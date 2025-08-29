from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from .models import CustomUser


def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    context = {"user": user}
    return render(request, "users/profile.html", context)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("tweets:home")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

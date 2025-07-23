from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm


def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    context = {'user': user}
    return render(request, 'users/profile.html', context)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tweet


def tweet_list_view(request):
    tweets = Tweet.objects.all()
    context = {'tweets': tweets}
    return render(request, 'tweets/tweet_list.html', context)

@login_required
def tweet_create_view(request):
    return render(request, 'tweets/tweet_create.html')

@login_required
def tweet_like_view(request, pk):
    return redirect('tweet_list')

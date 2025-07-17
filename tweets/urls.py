from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list_view, name='tweet_list'),
    path('create/', views.tweet_create_view, name='tweet_create'),
    path('<int:pk>/like/', views.tweet_like_view, name='tweet_like'),
]

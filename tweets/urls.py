from django.urls import path
from . import views

app_name = 'tweets'

urlpatterns = [
    path('', views.tweet_list_view, name='home'),
    path('create/', views.tweet_create_view, name='create'),
    path('<int:pk>/like/', views.tweet_like_view, name='tweet_like'),
]

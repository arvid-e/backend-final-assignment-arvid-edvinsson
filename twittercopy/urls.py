from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from users.views import SignUpView 


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    path('users/', include('users.urls')),
    path('tweets/', include('tweets.urls')),  
    path('followers/', include('followers.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home')
]

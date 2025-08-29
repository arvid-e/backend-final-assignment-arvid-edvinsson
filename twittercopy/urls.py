from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from users.views import SignUpView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "account/",
        include(
            (
                [
                    path("signup/", SignUpView.as_view(), name="signup"),
                    path("", include("django.contrib.auth.urls")),
                ],
                "account",
            ),
            namespace="account",
        ),
    ),
    path("users/", include("users.urls")),
    path("tweets/", include(("tweets.urls", "tweets"), namespace="tweets")),
    path("followers/", include("followers.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]

from django.conf import settings
from django.db import models


class Tweet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tweets",
    )
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_tweets", blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Tweet by {self.user.username} at "
            f"{self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )

    @property
    def number_of_likes(self):
        return self.likes.count()

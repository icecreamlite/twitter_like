from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)

    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return f'{self.username}: {self.email}'


class Tweet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tweets", on_delete=models.CASCADE)
    tweet_text = models.TextField(max_length=280)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes")

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.tweet_text
from django.db import models

from config.settings import AUTH_USER_MODEL


class Post(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField()

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Liked(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)

    is_liked = models.BooleanField(default=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class LikedItem(models.Model):
    liked_list = models.ForeignKey(Liked, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

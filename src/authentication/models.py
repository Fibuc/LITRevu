from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    followings = models.ManyToManyField(
        'self',
        through='UserFollows',
        related_name='followers',
        blank=True,
        symmetrical=False,
        )

    def __str__(self):
        return self.username
    

class UserFollows(models.Model):
    user = models.ForeignKey(User, related_name='following_relations', on_delete=models.CASCADE, verbose_name='Utilisateur')
    followed_user  = models.ForeignKey(User, related_name='follower_relations', on_delete=models.CASCADE, verbose_name='Utilisateur suivi')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Follows"
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user} suit {self.followed_user}"


from django.db import models
from django.contrib.auth.models import AbstractUser
from feed.models import Review, Ticket


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
    
    def get_users_viewable_reviews(self):
        all_reviews = Review.objects.filter(user__in=(self.followings.all())) | self.review_set.all()
        tickets = self.ticket_set.all()
        for ticket in tickets:
            # Ajout des reviews des utilisateurs non suivis.
            if ticket.review_set.all() not in all_reviews:
                all_reviews = all_reviews | ticket.review_set.all()

        return all_reviews

    def get_users_viewable_tickets(self):
        return Ticket.objects.filter(user__in=self.followings.all()) | self.ticket_set.all()
    

class UserFollows(models.Model):
    user = models.ForeignKey(User, related_name='following_relations', on_delete=models.CASCADE, verbose_name='Utilisateur')
    followed_user  = models.ForeignKey(User, related_name='follower_relations', on_delete=models.CASCADE, verbose_name='Utilisateur suivi')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Follows"
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user} suit {self.followed_user}"


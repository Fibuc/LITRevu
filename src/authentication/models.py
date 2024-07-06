from django.db import models
from django.contrib.auth.models import AbstractUser
from feed.models import Review, Ticket


class User(AbstractUser):
    """Modèle d'utilisateur personnalisé pour l'application."""
    followings = models.ManyToManyField(
        'self',
        through='UserFollows',
        related_name='followers',
        blank=True,
        symmetrical=False,
        )

    def __str__(self):
        """Retourne la représentation de l'utilisateur en chaînes de caractères."""
        return self.username

    def get_users_viewable_reviews(self):
        """Récupère et retourne toutes les critiques qui peuvent être visible pour l'utilisateur.

        Returns:
            QuerySet: Un queryset contenant toutes les critiques visibles pour l'utilisateur.
        """
        all_reviews = Review.objects.filter(user__in=(self.followings.all())) | self.review_set.all()
        tickets = self.ticket_set.all()
        for ticket in tickets:
            # Ajout des reviews des utilisateurs non suivis.
            if ticket.review_set.all() not in all_reviews:
                all_reviews = all_reviews | ticket.review_set.all()

        return all_reviews

    def get_users_viewable_tickets(self):
        """Récupère et retourne tous les tickets qui peuvent être visible pour l'utilisateur.

        Returns:
            QuerySet: Un queryset contenant tous les tickets visibles pour l'utilisateur.
        """
        return Ticket.objects.filter(user__in=self.followings.all()) | self.ticket_set.all()


class UserFollows(models.Model):
    """Modèle des relations des suivis d'utilisateur."""
    user = models.ForeignKey(
        User, related_name='following_relations', on_delete=models.CASCADE, verbose_name='Utilisateur'
        )
    followed_user = models.ForeignKey(
        User, related_name='follower_relations', on_delete=models.CASCADE, verbose_name='Utilisateur suivi'
        )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Follows"
        unique_together = ('user', 'followed_user')

    def __str__(self):
        """Retourne la représentation du suivi utilisateur en chaînes de caractères."""
        return f"{self.user} suit {self.followed_user}"

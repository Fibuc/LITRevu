from django.contrib import admin
from .models import User, UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    """Classe permettant de personnaliser l'affichage des suivis utilisateur dans l'interface d'administration."""
    list_display = ('user', 'followed_user', 'created_at')


class UserAdmin(admin.ModelAdmin):
    """Classe permettant de personnaliser l'affichage des utilisateurs dans l'interface d'administration."""
    list_display = ('username', 'date_joined')


admin.site.register(User, UserAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)

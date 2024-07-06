from django.contrib import admin
from .models import Ticket, Review


class ReviewAdmin(admin.ModelAdmin):
    """Classe permettant de personnaliser l'affichage des critiques dans l'interface d'administration."""
    list_display = ('headline', 'user', 'rating', 'time_created', 'ticket')


class TicketAdmin(admin.ModelAdmin):
    """Classe permettant de personnaliser l'affichage des tickets dans l'interface d'administration."""
    list_display = ('title', 'user', 'time_created')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Ticket, TicketAdmin)

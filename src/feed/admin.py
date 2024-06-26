from django.contrib import admin
from .models import Ticket, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'user', 'rating', 'time_created')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Ticket, TicketAdmin)
from django.contrib import admin
from .models import User, UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user', 'created_at')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined')

admin.site.register(User, UserAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
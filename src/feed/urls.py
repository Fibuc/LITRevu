from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('follows/', views.followed_user, name='follows'),
    path('follows/follow/<int:user_id>/', views.follow_user, name='follow'),
    path('follows/unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),
    path('posts/', views.posts, name='posts'),
    path('posts/ticket/', views.create_ticket, name='create_ticket'),
    path('posts/ticket/valid/', views.valid_ticket, name='valid_ticket'),
    path('posts/review/', views.create_ticket_review, name='create_ticket_review'),
    path('posts/review/valid/', views.valid_ticket_review, name='valid_ticket_review'),
]
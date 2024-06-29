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
    path('posts/ticket/<int:ticket_id>/modify/', views.modify_ticket, name='modify_ticket'),
    path('posts/ticket/<int:ticket_id>/delete/', views.confirm_delete_ticket, name='delete_ticket'),
    path('posts/ticket/<int:ticket_id>/review/', views.create_review, name='create_review'),
    path('posts/review/', views.create_ticket_review, name='create_ticket_review'),
    path('posts/review/valid/', views.valid_review, name='valid_review'),
    path('posts/review/<int:review_id>/modify/', views.modify_review, name='modify_review'),
    path('posts/review/<int:review_id>/delete/', views.confirm_delete_review, name='delete_review'),
    path('posts/delete_confirmation/', views.delete_confirmation, name='delete_confirmation'),
    path('posts/not_found/', views.element_not_found, name='not_found'),
]
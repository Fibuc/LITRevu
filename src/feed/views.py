from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.forms import formset_factory
from authentication.models import UserFollows
from feed.models import Ticket, Review
from itertools import chain
from . import forms

User = get_user_model()

@login_required
def followed_user(request):
    user = request.user
    followings = user.following_relations.all()
    followers = user.follower_relations.all()
    form = forms.UserSearchForm()

    if 'search_user' in request.GET:
        form = forms.UserSearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search_user']
            search_results = User.objects.filter(username__icontains=search).exclude(username=request.user.username)
            if search:
                return render(
                    request,
                    'feed/follows.html',
                    {   
                        'search_user': search,
                        'followings': followings,
                        'followers': followers,
                        'form': form,
                        'search_results': search_results
                    })

    return render(
        request,
        'feed/follows.html',
        {
            'followings': followings,
            'followers': followers,
            'form': form,
        }
    )

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow)
    return redirect('follows')

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()
    return redirect('follows')

@login_required
def feed(request):
    return render(request, 'feed/feed.html')

@login_required
def posts(request):
    user = request.user
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    all_posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created,
        reverse=True
        )
    return render(request, 'feed/posts.html', {'user': user, 'all_posts': all_posts})

@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('valid_ticket')

    return render(request, 'feed/create_ticket.html', {'form': form})

@login_required
def create_ticket_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            review = review_form.save(commit=False)

            ticket.user = review.user = request.user
            review.ticket = ticket

            ticket.save()
            review.save()
            return redirect('valid_ticket_review')

    return render(request, 'feed/create_review.html', {'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def valid_ticket(request):
    return render(request, 'feed/valid_ticket.html')

@login_required
def valid_ticket_review(request):
    return render(request, 'feed/valid_review.html')
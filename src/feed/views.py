from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import CharField, Value, BooleanField
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import UserFollows, User
from feed.models import Ticket, Review
from itertools import chain
from . import forms


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
def feed(request):
    user = get_object_or_404(User, id=request.user.id)
    reviews = user.get_users_viewable_reviews()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = user.get_users_viewable_tickets()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # Si utilisateur a déjà répondu.
    for ticket in tickets:
        if responses := ticket.review_set.all():
            for response in responses:
                already_response = False
                if response.user == request.user:
                    already_response = True
                    break

        ticket.already_response = already_response

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'feed/feed.html', {'posts': posts})


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
def posts(request):
    user = request.user
    tickets = Ticket.objects.all().filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = Review.objects.all().filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    all_user_posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created,
        reverse=True
        )

    return render(request, 'feed/posts.html', {'all_user_posts': all_user_posts})

@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Votre ticket a été créé avec succès!')
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
            messages.success(request, 'Votre critique a été créée avec succès!')
            return redirect('valid_review')

    return render(request, 'feed/create_review.html', {'ticket_form': ticket_form, 'review_form': review_form})


def create_review(request, ticket_id):
    review_form = forms.ReviewForm()
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Votre critique a été créée avec succès!')
            return redirect('valid_review')
        
    return render(request, 'feed/create_review.html', {'review_form': review_form, 'post': ticket})


@login_required
def valid_ticket(request):
    return render(request, 'feed/valid_ticket.html')

@login_required
def valid_review(request):
    return render(request, 'feed/valid_review.html')

@login_required
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Vérification si l'utilisateur connecté est bien le créateur du ticket.
    if ticket.user != request.user:
        return redirect('not_found')

    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre ticket a été modifié avec succès!')
            return redirect('valid_ticket')
    
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, 'feed/modify_ticket.html', {'form': form})


@login_required
def modify_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    # Vérification si l'utilisateur connecté est bien le créateur du ticket.
    if review.user != request.user:
        return redirect('not_found')

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre critique a été modifiée avec succès!')
            return redirect('valid_review')
    
    else:
        form = forms.ReviewForm(instance=review)

    return render(request, 'feed/modify_review.html', {'form': form, 'post': review.ticket})


@login_required
def element_not_found(request):
    return render(request, 'feed/element_not_found.html')


@login_required
def confirm_delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return redirect('not_found')

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Le ticket a bien été supprimé.')
        return redirect('delete_confirmation')
    
    return render (request, 'feed/confirm_delete_ticket.html', {'post': ticket})

@login_required
def confirm_delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return redirect('not_found')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'La critique a bien été supprimée.')
        return redirect('delete_confirmation')
    
    return render (request, 'feed/confirm_delete_review.html', {'post': review})


def delete_confirmation(request):
    return render(request, 'feed/delete_confirmation.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import UserFollows, User
from feed.models import Ticket, Review
from itertools import chain
from . import forms


@login_required
def followed_user(request):
    """Vue qui affiche le menu du suivi utilisateur.

    Args:
        request (HttpRequest): Requête avec les informations des liens entre les utilisateurs.

    Returns:
        HttpResponse: La page HTML avec les informations des liens avec l'utilisateurs.
    """
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
    """Vue qui affiche le fil d'actualité des posts de l'utilisateur.

    Args:
        request (HttpRequest): Requête avec les posts visibles pour l'utilisateur.

    Returns:
        HttpResponse: La page HTML avec les posts visibles pour l'utilisateurs.
    """
    already_response = None
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

    # Tri des posts dans l'ordre du plus récent.
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'feed/feed.html', {'posts': posts})


@login_required
def follow_user(request, user_id):
    """Vue qui permet de suivre un utilisateur.

    Args:
        request (HttpRequest): Requête l'ID de l'utilisateur à suivre.
        user_id (int): ID de l'utilisateur.

    Returns:
        HttpResponse: La page HTML pour valider le suivi d'un utilisateur.
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow)
    return redirect('follows')


@login_required
def unfollow_user(request, user_id):
    """Vue qui permet de ne plus suivre un utilisateur.

    Args:
        request (HttpRequest): Requête l'ID de l'utilisateur à ne plus suivre.
        user_id (int): ID de l'utilisateur.

    Returns:
        HttpResponse: La page HTML pour retirer le suivi d'un utilisateur.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()
    return redirect('follows')


@login_required
def posts(request):
    """Vue qui affiche les différents posts de l'utilisateur.

    Args:
        request (HttpRequest): Requête avec les posts de l'utilisateur.

    Returns:
        HttpResponse: La page HTML avec les posts de l'utilisateurs.
    """
    user = request.user
    tickets = Ticket.objects.all().filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = Review.objects.all().filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    # Tri des posts dans l'ordre du plus récent.
    all_user_posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created,
        reverse=True
        )

    return render(request, 'feed/posts.html', {'all_user_posts': all_user_posts})


@login_required
def create_ticket(request):
    """Vue qui permet de créer un ticket si les informations entrées sont correctes.

    Args:
        request (HttpRequest): Requête avec les informations du ticket à créer.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de confirmation de création.
    """
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
    """Vue qui permet de créer un ticket et une critique en même temps si les informations entrées sont correctes.

    Args:
        request (HttpRequest): Requête avec les informations de la critique à créer.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de confirmation de création.
    """
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


@login_required
def create_review(request, ticket_id):
    """Vue qui permet de créer une critique en réponse à un ticket si les informations entrées sont correctes.

    Args:
        request (HttpRequest): Requête avec les informations de la critique à créer.
        ticket_id (int): ID du ticket correspondant à la critique.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de confirmation de création.
    """
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
    """Vue qui affiche la confirmation de création du ticket.

    Args:
        request (HttpRequest): Requête avec la validation de création.

    Returns:
        HttpResponse: La page HTML pour afficher le message de validation à l'utilisateur.
    """
    return render(request, 'feed/valid_ticket.html')


@login_required
def valid_review(request):
    """Vue qui affiche la confirmation de création de la critique.

    Args:
        request (HttpRequest): Requête avec la validation de création.

    Returns:
        HttpResponse: La page HTML pour afficher le message de validation à l'utilisateur.
    """
    return render(request, 'feed/valid_review.html')


@login_required
def modify_ticket(request, ticket_id):
    """Vue qui permet de modifier les informations d'un ticket.

    Args:
        request (HttpRequest): Requête avec les informations du ticket à modifier.
        ticket_id (int): ID du ticket.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de validation de modification.
    """
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

    return render(request, 'feed/modify_ticket.html', {'form': form, 'post': ticket})


@login_required
def modify_review(request, review_id):
    """Vue qui permet de modifier les informations d'une critique.

    Args:
        request (HttpRequest): Requête avec les informations de la critique à modifier.
        review_id (int): ID de la critique.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de validation de modification.
    """
    review = get_object_or_404(Review, id=review_id)
    # Vérification si l'utilisateur connecté est bien le créateur de la critique.
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
    """Vue qui permet de notifier l'utilisateur que l'élément est introuvable.

    Args:
        request (HttpRequest): Requête avec l'élément recherché.

    Returns:
        HttpResponse: La page HTML avec le message à l'utilisateur.
    """
    return render(request, 'feed/element_not_found.html')


@login_required
def confirm_delete_ticket(request, ticket_id):
    """Vue qui permet de demander la confirmation de suppression d'un ticket à l'utilisateur.

    Args:
        request (HttpRequest): Requête avec les informations du ticket à supprimer.
        ticket_id (int): ID du ticket.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de validation de suppression.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return redirect('not_found')

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Votre ticket a bien été supprimé.')
        return redirect('delete_confirmation')

    return render(request, 'feed/confirm_delete_ticket.html', {'post': ticket})


@login_required
def confirm_delete_review(request, review_id):
    """Vue qui permet de demander la confirmation de suppression d'une critique à l'utilisateur.

    Args:
        request (HttpRequest): Requête avec les informations de la critique à supprimer.
        review_id (int): ID de la critique.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de validation de suppression.
    """
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return redirect('not_found')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Votre critique a bien été supprimée.')
        return redirect('delete_confirmation')

    return render(request, 'feed/confirm_delete_review.html', {'post': review})


@login_required
def delete_confirmation(request):
    """Vue qui affiche la confirmation de suppresion de l'élément.

    Args:
        request (HttpRequest): Requête avec la validation de supression.

    Returns:
        HttpResponse: La page HTML pour afficher le message de suppression à l'utilisateur.
    """
    return render(request, 'feed/delete_confirmation.html')

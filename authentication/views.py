from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models 
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from ecommerce.models import Article, Photo, Commande, Quantite
from django.contrib.auth.models import User


def signup(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,'authentication/signup.html', context={'form':form})


@login_required
def count(request):
    user = request.user
    commandes = Commande.objects.filter(buyer=user)
    commandes1 =[]
    for commande in commandes:
        if commande.payed == True :
            quantites = Quantite.objects.filter(commande=commande)
            prix = 0
            for quantite in quantites:
                prix += quantite.article.price*quantite.nombre
            quantites.prix = prix
            commandes1.append(quantites)
    publications1 = Article.objects.filter(seller=user.id)
    publications = sorted(publications1, key=lambda instance: instance.date_created, reverse=True)
    nb_publications = len(publications)
    nb_likes = 0
    for article in publications :
        article.image_principal = Photo.objects.filter(article=article.id).first()
        nb_likes = nb_likes + article.likes.count()
    nb_followers = 0
    for user in get_user_model().objects.all():
        if user.follows.filter(id=user.id).exists():
            nb_followers += 1
    user.nb_likes = nb_likes
    user.nb_followers = nb_followers
    user.nb_publications = nb_publications
    if request.method == 'POST':
        if request.POST.get('cmdp'):
            return redirect('password-change')
        elif request.POST.get('logout'):
            return redirect ('logout')
        elif request.POST.get('unfollow'):
            print(request.POST.get('data-personne-id'))
            personne =get_object_or_404(get_user_model(),id=request.POST.get('data-personne-id'))
            request.user.follows.remove(personne)
            return redirect ('count')
    return render(request, 'authentication/count.html', context={'user':user, 'publications':publications, 'commandes':commandes1})

@login_required
def change_photo_profile(request):
    form = forms.UploadProfilePhotoForm()
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('count')
    return render(request,'authentication/change_photo_profile.html', context={'form': form})

@login_required
def change_username(request):
    form = forms.UploadUsernameForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('count')
    return render(request,'authentication/change_username.html', context={'form': form})


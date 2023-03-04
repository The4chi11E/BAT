from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models
from django.conf import settings
from django.contrib.auth import get_user_model
from .decorators import article_creator

def home(request):
    nb_article_en_cours={}
    if request.user.is_authenticated :
        if models.Commande.objects.filter(buyer=request.user).exists():
            if models.Commande.objects.filter(buyer=request.user).last().payed == False:
                commande_en_cours = models.Commande.objects.filter(buyer=request.user).last()
                nb_article_en_cours = models.Quantite.objects.filter(commande=commande_en_cours).count()
    if request.method == 'POST':
        return redirect('view-article')
    return render (request,'ecommerce/index.html', context={'nb_article_en_cours':nb_article_en_cours})

def support(request):
    return render(request,'ecommerce/support.html')

def cata_articles(request):
    articles = models.Article.objects.all()
    article1 = sorted(articles, key=lambda instance: instance.date_created, reverse=True)
    for article in article1 :
        article.image_principal = models.Photo.objects.filter(article=article.id).first()
    return render(request, 'ecommerce/cata_blog.html', context={'articles':article1})

@login_required
def post(request):
    formA = forms.ArticleForm()
    formP = forms.PhotoForm()

    if request.method == 'POST':
        formA = forms.ArticleForm(request.POST)
        formP = forms.PhotoForm(request.POST, request.FILES)
        if formA.is_valid() and formP.is_valid():
            article = formA.save(commit=False)
            article.seller = request.user
            article.save()
            for image in request.FILES.getlist('image'):
                models.Photo.objects.create(article=article, image=image)
            return redirect('view-article')
    return render(request,'ecommerce/post.html', context={'formA':formA, 'formP':formP})


def detail_article(request,pk):
    article = get_object_or_404(models.Article, id=pk)
    form_avis = forms.AvisForm()
    form_delete_avis = forms.DeleteCommentForm()
    images = models.Photo.objects.filter(article=pk)
    avis = models.Avis.objects.filter(article=pk)
    form_quantite = forms.CommandeForm()

    if request.method == 'POST':
        if request.POST.get('avis'):
            form_avis = forms.AvisForm(request.POST)
            if form_avis.is_valid():
                avis = form_avis.save(commit=False)
                avis.author = request.user
                avis.article = article
                form_avis.save()
                return redirect('detail-article',pk=pk)

        elif request.POST.get('delete_avis'):
            form_delete_avis = forms.DeleteCommentForm(request.POST)
            if form_delete_avis.is_valid():
                avis_id = request.POST.get('avi_id')
                avis = get_object_or_404(models.Avis, id=avis_id)
                avis.delete()
                return redirect('detail-article', pk=pk)

        elif request.POST.get('edit_article'):
                return redirect('edit-delete-article',pk=pk)

        elif request.POST.get('like'):
            if article.likes.filter(id=request.user.id).exists():
                article.likes.remove(request.user)
                return redirect('detail-article', pk=pk)
            else:
                article.likes.add(request.user)
                return redirect('detail-article', pk=pk) 
            
        elif request.POST.get('command'):
            if request.user.is_authenticated:
                i = request.POST.get('nombre')
                current_order = models.Commande.objects.filter(buyer=request.user).last()
                if models.Commande.objects.filter(buyer=request.user).exists() :
                    if current_order.payed == False:
                        nombre = models.Quantite(nombre=i)
                        nombre.article = article
                        nombre.commande = current_order
                        nombre.save()
                    else:
                        nombre = models.Quantite(nombre=i)
                        commande = models.Commande.objects.create(buyer=request.user)
                        nombre.article = article
                        nombre.commande = commande
                        nombre.save()
                        commande.articles.add(nombre)
                else : 
                    nombre = models.Quantite(nombre=i)
                    commande = models.Commande.objects.create(buyer=request.user)
                    nombre.article = article
                    nombre.commande = commande
                    nombre.save()
                    commande.articles.add(nombre)
                return redirect('view-article')
            else:
                return redirect('login')

    return render(request,'ecommerce/article_detail.html', context = {
            'form_avis':form_avis,
            'article':article, 
            'images':images, 
            'avis':avis,
            'form_delete_comment':form_delete_avis,
            'form_quantite':form_quantite,
        })


@login_required
@article_creator
def edit_supp_article(request,pk):
    article = get_object_or_404(models.Article, id=pk)
    photo_article = article.photo_set.all()
    edit_formA = forms.ArticleForm(instance=article)
    form_photo =[]
    for photo in photo_article:
        form_photo.append(forms.PhotoForm(instance=photo))
    delete_form = forms.DeleteArticleForm()
    if request.method == 'POST':
        if request.POST.get('edit'):
            edit_formA = forms.ArticleForm(request.POST,instance=article)
            if edit_formA.is_valid():
                article = edit_formA.save(commit=False)
                article.seller = request.user
                article.save()
                form_photo =[]
                for photo in photo_article:
                    form_photo.append(forms.PhotoForm(request.POST, request.FILES,instance=article))
                photo_article.delete()
                for form in form_photo:
                    if form.is_valid():
                        for image in request.FILES.getlist('image'):
                            models.Photo.objects.create(article=article, image=image)
                        return redirect('detail-article', pk=pk)
        if request.POST.get('delete'):
            delete_form = forms.DeleteArticleForm(request.POST)
            if delete_form.is_valid():
                article = models.Article.objects.filter(id=pk).first()
                photo_article = models.Photo.objects.filter(article=pk).all()
                article.delete()
                photo_article.delete()
                return redirect('view-article')
    return render(request,'ecommerce/edit_article.html', context={'edit_formA':edit_formA,'edit_formP':form_photo, 'delete_form': delete_form})


def search_user(request):
    users = get_user_model().objects.all()
    return render(request,'ecommerce/search_user.html', context={'users':users})

def user_detail(request,user_id):
    user_detail = get_object_or_404(get_user_model(),id=user_id)

    publications1 = models.Article.objects.filter(seller=user_detail.id)
    publications = sorted(publications1, key=lambda instance: instance.date_created, reverse=True)
    nb_publications = len(publications)
    nb_likes = 0
    for article in publications :
        article.image_principal = models.Photo.objects.filter(article=article.id).first()
        nb_likes = nb_likes + article.likes.count()
    nb_followers = 0
    for user in get_user_model().objects.all():
        if user.follows.filter(id=user_id).exists():
            nb_followers += 1

    follow = False
    if request.user.follows.filter(id=user_id).exists():
        follow = True
    if request.method =='POST':
        if request.POST.get('follow'):
            if request.user.follows.filter(id=user_id).exists():
                request.user.follows.remove(user_detail)
                return redirect ('user-detail', user_id=user_id)
            
            else:
                request.user.follows.add(user_detail)
                return redirect ('user-detail', user_id=user_id)
    return render(request,'ecommerce/user_detail.html', context={'follow':follow,'nb_followers':nb_followers ,'user':user_detail, 'publications':publications, 'nb_publications':nb_publications, 'nb_likes':nb_likes})


@login_required
def panier(request):
    commande = models.Commande.objects.filter(buyer=request.user).last()
    articles = models.Quantite.objects.filter(commande=commande)
    prix = 0
    for article in articles:
        article.form = forms.CommandeForm(instance=article)
        article_prix = article.prix()
        prix = prix + article_prix
    if request.method == 'POST':
        if request.POST.get('change-order'):
                models.Quantite.objects.filter(id=request.POST.get('data-quantite-id')).update(nombre=request.POST.get('nombre'))
                return redirect('panier')
        if request.POST.get('delete-order'):
                models.Quantite.objects.filter(id=request.POST.get('data-quantite-id')).delete()
                return redirect('panier')
        if request.POST.get('paiement'):
            return redirect('paiement')
        if request.POST.get('delete'):
            commande.delete()
            return redirect('view-article')
    context={
        'commande':commande,
        'articles':articles,
        'prix':prix
             }
    return render(request,'ecommerce/panier.html', context)

@login_required
def paiement(request):
    commande = models.Commande.objects.filter(buyer=request.user).last()
    context={}
    return render(request, 'ecommerce/paiement.html',context)
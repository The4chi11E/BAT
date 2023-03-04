from . import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect


def article_creator(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        article = get_object_or_404(models.Article, id=pk)
        if request.user == article.seller:
            return view_func(request, pk,*args, **kwargs)
        else:
            return HttpResponse('You are not authorized to change this article.')
    return wrapper_func



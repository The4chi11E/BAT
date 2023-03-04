from django.db import models
from django.db import models
from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from  django.contrib.auth.models import User
from decimal import Decimal

User1 = get_user_model()

def validate_seller(value):
    if not isinstance(value, User1) or not hasattr(value, 'customuser'):
        raise ValidationError('Le vendeur doit être un objet CustomUser')

def validate_author(value):
    if not isinstance(value, User1) or not hasattr(value, 'customuser'):
        raise ValidationError('Autheur doit être un objet CustomUser')



class Article(models.Model):
    title = models.CharField(max_length=100)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,validators=[validate_seller])
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)


class Photo(models.Model):
    image = models.ImageField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    IMAGE_MAX_SIZE = (800,800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        self.resize_image()

def validate_article(value):
    if not isinstance(value, Article):
        raise ValidationError('Article doit être un objet Article')


class Avis(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)

class Commande(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='Quantite')
    date = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)

class Quantite(models.Model): 
    nb_choices = [(i,i) for i in range(1,100)] 
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE) 
    article = models.ForeignKey(Article, on_delete=models.CASCADE) 
    nombre = models.IntegerField(choices=nb_choices)

    def prix(self):
        prix = Decimal(self.article.price)*Decimal(self.nombre)
        return prix

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        self.prix = self.prix()



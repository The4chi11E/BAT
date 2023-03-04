from django.contrib import admin
from authentication.models import CustomUser
from ecommerce.models import Photo, Article, Avis, Commande, Quantite

admin.site.register(CustomUser)
admin.site.register(Avis)
admin.site.register(Article)
admin.site.register(Photo)
admin.site.register(Commande)
admin.site.register(Quantite)

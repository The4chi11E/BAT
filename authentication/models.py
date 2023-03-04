from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

class CustomUser(AbstractUser):
    photo_profile = models.ImageField(default='default_utilisateur.png')
    follows = models.ManyToManyField(
        'self',
        symmetrical=False
    )
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions',blank=True)

    IMAGE_MAX_SIZE = (800,800)

    def resize_image(self):
        image = Image.open(self.photo_profile)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.photo_profile.path)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        self.resize_image()



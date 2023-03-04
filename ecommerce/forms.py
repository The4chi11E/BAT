from django import forms
from django.contrib.auth import get_user_model
from . import models
from authentication.models import CustomUser

class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'price', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'})
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']
        widgets = {
            'image' : forms.ClearableFileInput(attrs={'multiple':True})
        }

class AvisForm(forms.ModelForm):
    class Meta:
        model = models.Avis
        fields = ['comment']



class FollowUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['follows']

class CommandeForm(forms.ModelForm):
    class Meta:
        model = models.Quantite
        fields = ['nombre']

class DeleteArticleForm(forms.Form):
    delete_Article = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class DeleteCommentForm(forms.Form):
    delete_Comment = forms.BooleanField(widget=forms.HiddenInput, initial=True)    
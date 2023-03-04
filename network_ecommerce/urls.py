"""reseau_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import(
    LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
)
from django.conf import settings
from django.conf.urls.static import static
import ecommerce.views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Bat:reseau_e-commerce/' or '', ecommerce.views.home, name='home' ),
    path('', ecommerce.views.home, name='home1' ),
    path('login/', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'
    ), name='password-change-done'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='authentication/password_change.html'
    ), name='password-change'),
    path('signup/',authentication.views.signup, name='signup'),
    path('support/', ecommerce.views.support, name='support'),
    path('articles/', ecommerce.views.cata_articles, name='view-article'),
    path('post/', ecommerce.views.post, name='post'),
    path('count/', authentication.views.count, name='count'),
    path('article:<int:pk>', ecommerce.views.detail_article,name='detail-article'),
    path('search-user/', ecommerce.views.search_user, name='search-user'),
    path('user:<int:user_id>', ecommerce.views.user_detail, name='user-detail'),
    path('change-photo-profile/', authentication.views.change_photo_profile, name='change-photo-profile'),  
    path('change-username/', authentication.views.change_username, name='change-username'),
    path('edit-supp-article:<int:pk>', ecommerce.views.edit_supp_article, name='edit-delete-article'),
    path('reset-password/',PasswordResetView.as_view(), name='password-reset' ),
    path('reset-password-sent/',PasswordResetDoneView.as_view(),name='password_reset_done' ),
    path('reset<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm' ),
    path('reset-password-complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete' ),
    path('order/', ecommerce.views.panier, name='panier'),
    path('paiement/', ecommerce.views.paiement, name='paiement'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
def my_context_processor(request):
    return {
    'show_accueil_login': True if request.path.startswith('/login/') or
        request.path.startswith('/signup/') else False,
    'show_accueil_support': True if request.path.startswith('/support/') else False,
    'show_accueil_articles': True if request.path.startswith('/articles/') else False,
    'show_accueil_post': True if request.path.startswith('/post/') else False,
    'show_accueil_count': True if request.path.startswith('/count/') or
        request.path.startswith('/change-password/') else False,
    }
def test(request):
    return {
        'accueil': True if request.path.startswith('/support/') else False 
    }
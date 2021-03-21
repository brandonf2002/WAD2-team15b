from django.shortcuts import render

def index(request):
    return render(request, 'meme_portal/index.html')
    
def create_page(request, category_name_slug):
    return render(request, 'meme_portal/create.html')
    
def register(request):
    return render(request, 'meme_portal/register.html')
    
def user_login(request):
    return render(request, 'meme_portal/login.html')
    
def user_logout(request):
    return render(request, 'meme_portal/logout.html')
    
def user_account(request):
    return render(request, 'meme_portal/account.html')
    
def create(request):
    return render(request, 'meme_portal/create.html')

def forum(request):
    return render(request, 'meme_portal/forum.html')

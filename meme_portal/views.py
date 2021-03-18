from django.shortcuts import render

def index(request):
    return render(request, 'meme_portal/index.html')

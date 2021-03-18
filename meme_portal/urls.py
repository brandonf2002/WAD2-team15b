from django.urls import path
from meme_portal import views

app_name = 'meme_portal'

urlpatterns = [
    path('', views.index, name='meme_portal_index')
]

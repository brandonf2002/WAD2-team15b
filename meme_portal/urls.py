from django.urls import path
from meme_portal import views

app_name = 'meme_portal'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create, name='create'),
    path('account/', views.user_account, name='account'),
    path('forum/<slug:forum_name_slug>/', views.show_forum, name='show_forum'),
    path('forum/', views.forum, name='forum'),
    path('forum/<slug:forum_name_slug>/create_post/', views.create_post, name='create_post'),
]

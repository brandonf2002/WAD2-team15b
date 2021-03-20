from django.urls import path
from meme_portal import views

app_name = 'meme_portal'

urlpatterns = [
    path('', views.index, name='meme_portal_index'),
	path('register/', views.register, name='register'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout,name='logout'),
	path('create/', views.user_logout,name='create'),
]

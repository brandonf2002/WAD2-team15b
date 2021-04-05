from django.urls import path
from meme_portal import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'meme_portal'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_post, name='create_post'),
    path('createpage/', views.create_page, name='create_page'),
    path('account/', views.user_account, name='account'),
    path('forum/<slug:forum_name_slug>/', views.show_forum, name='show_forum'),
    path('forum/<slug:forum_name_slug>/sort_by/<sort_by>/', views.show_forum, name='show_forum_sort'),
    path('forum/', views.forum, name='forum'),
    path('forum/<slug:forum_name_slug>/create_post/', views.create_post, name='create_post'),
    path('forum/<slug:forum_name_slug>/<slug:post_name_slug>', views.show_post, name='show_post'),
    path('forum/<slug:forum_name_slug>/<slug:post_name_slug>/delete', views.delete_post, name='delete_post'),
    path('forum/<slug:forum_name_slug>/<slug:post_name_slug>/like', views.like_link, name='like_post'),
    path('forum/<slug:forum_name_slug>/<slug:post_name_slug>/dislike', views.dislike_link, name='dislike_post'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='meme_portal/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="meme_portal/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='meme_portal/password/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

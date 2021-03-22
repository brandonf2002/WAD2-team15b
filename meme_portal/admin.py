from django.contrib import admin
from meme_portal.models import Forum, Post, Comment, UserProfile

admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)


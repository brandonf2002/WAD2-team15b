from django.contrib import admin
from meme_portal.models import Forum, Post, Comment, UserProfile

class ForumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Forum, ForumAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)


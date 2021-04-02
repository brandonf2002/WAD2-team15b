from django import forms
from django.contrib.auth.models import User
from meme_portal.models import Forum, UserProfile, Post, Comment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('name','img_url')

class ForumForm(forms.ModelForm):
    class Meta:
        model=Forum
        fields=('name', )

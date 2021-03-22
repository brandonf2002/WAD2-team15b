from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Forum(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name;

class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    img_url = models.URLField()
    time_posted = models.DateTimeField(default=timezone.now)
    ##########  RE_INSTATE ONCE USERS CAN BE CREATED  ################
    #author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name;

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    time_posted = models.DateTimeField(default=timezone.now)
    ##########  RE_INSTATE ONCE USERS CAN BE CREATED  ################
    #author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# The additional attributes we wish to include.
	email = models.EmailField(blank=True)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	
	def __str__(self):
		return self.user.username


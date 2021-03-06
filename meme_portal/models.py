from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, related_name='userProfile')
	# The additional attributes we wish to include.
	email = models.EmailField(blank=True)
	picture = models.ImageField(default="profile1.png", upload_to='profile_images', blank=True)

	def __str__(self):
		return str(self.user)

class Forum(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True);

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def __str__(self):
        return self.name;

class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts')
    name = models.CharField(max_length=128)
    img_url = models.URLField()
    time_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(UserProfile, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(UserProfile, related_name='dislikes', blank=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.name;

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    time_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

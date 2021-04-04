from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, ForumForm, UserForm, UserProfileForm
from meme_portal.forms import UserForm, UserProfileForm, PostForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import RedirectView
from meme_portal.models import Post, Forum, Comment, UserProfile
from datetime import datetime
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages

def index(request):
    forums_with_posts = Forum.objects.filter(posts__isnull=False).distinct()
    forum_list = []

    # Weird solution to assure that all forums displayed on index page have
    # at least some post, works however
    for i in range(max(5, len(forums_with_posts))):
        x = forums_with_posts.order_by('?').first()
        while x in forum_list:
            x = forums_with_posts.order_by('?').first()
        forum_list.append(x)

    # here we add the top 3 posts to the a dict to be passed to the index page
    forum_data = []
    for i in forum_list:
        forum_data.append(
            {
                'forum': i,
                'posts': Post.objects.filter(forum=i).annotate(like_count=Count('likes')).order_by('-like_count')[:3]
            }
        )

    context_dict = {
        'forum_data': forum_data
    }
    return render(request, 'meme_portal/index.html', context=context_dict)

def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):
	# Get the number of visits to the site.
	# We use the COOKIES.get() function to obtain the visits cookie.
	# If the cookie exists, the value returned is casted to an integer.
	# If the cookie doesn't exist, then the default value of 1 is used.
	visits = int(request.COOKIES.get('visits', '1'))
	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		# Update the last visit cookie now that we have updated the count
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie

	request.session['visits'] = visits

def register(request):
    # A boolean value for telling the template
	# whether the registration was successful.
	# Set to False initially. Code changes value to
	# True when registration succeeds.
	registered = False
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

                        # Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves,
			# we set commit=False. This delays saving the model

			# until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and
			#put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now we save the UserProfile model instance.
			profile.save()
			# Update our variable to indicate that the template
			# registration was successful.
			registered = True
		else:
			# Invalid form or forms - mistakes or something else?
			# Print problems to the terminal.
			print(user_form.errors, profile_form.errors)
	else:
		# Not a HTTP POST, so we render our form using two ModelForm instances.
		# These forms will be blank, ready for user input.
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context.
	return render(request,
					'meme_portal/register.html',
					context = {'user_form': user_form,
					'profile_form': profile_form,})

def user_login(request):
# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# We use request.POST.get('<variable>') as opposed
		# to request.POST['<variable>'], because the
		# request.POST.get('<variable>') returns None if the
		# value does not exist, while request.POST['<variable>']
		# will raise a KeyError exception.
		username = request.POST.get('username')
		password = request.POST.get('password')
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return redirect(reverse('meme_portal:index'))
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your Meme_portal account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
			# The request is not a HTTP POST, so display the login form.

		# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'meme_portal/login.html')

@login_required(login_url='login')
def user_account(request):
    visitor_cookie_handler(request)
    userprofile=request.user.userProfile
    form=UserProfileForm(instance=userprofile)
    context_dict = {'form':form}

    if request.method== 'POST':
        form=UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()


    return render(request, 'meme_portal/account.html', context=context_dict)

def show_forum(request, forum_name_slug):
    context_dict = {}

    try:
        forum = Forum.objects.get(slug=forum_name_slug)
        posts = Post.objects.filter(forum=forum)

        context_dict['posts'] = posts
        context_dict['forum'] = forum
    except Forum.DoesNotExist:
        context_dict['posts'] = None
        context_dict['forum'] = None

    return render(request, 'meme_portal/forum.html', context=context_dict)

def forum(request):
    forum_slug = Forum.objects.order_by('?')[0].slug
    return show_forum(request, forum_slug)

def show_post(request, forum_name_slug, post_name_slug):
    context_dict = {}

    post = get_object_or_404(Post, slug=post_name_slug)
    forum = get_object_or_404(Forum, slug=forum_name_slug)
    comments = post.comments.all().order_by('-time_posted')
    new_comment = None

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            user = get_object_or_404(UserProfile, user=request.user)
            new_comment.post = post
            new_comment.author = user
            new_comment.save()
            return redirect(reverse('meme_portal:show_post', kwargs={"forum_name_slug":forum_name_slug, "post_name_slug":post_name_slug}))
    else:
        comment_form = CommentForm()

    context_dict['post'] = post
    context_dict['forum'] = forum
    context_dict['comments'] = comments
    context_dict['comment_forum'] = comment_form
    return render(request=request, template_name='meme_portal/post.html', context=context_dict)

@login_required
def like_link(request, forum_name_slug, post_name_slug):
    if request.method == 'GET':
        usr = request.user
        post = get_object_or_404(Post, slug=post_name_slug)
        usrProf = get_object_or_404(UserProfile, user=usr)
        if usr.is_authenticated:
            if usrProf in post.likes.all():
                post.likes.remove(usrProf)
            else:
                if usrProf in post.dislikes.all():
                    post.dislikes.remove(usrProf)
                post.likes.add(usrProf)
    return show_forum(request, forum_name_slug)

@login_required
def dislike_link(request, forum_name_slug, post_name_slug):
    if request.method == 'GET':
        usr = request.user
        post = get_object_or_404(Post, slug=post_name_slug)
        usrProf = get_object_or_404(UserProfile, user=usr)
        if usr.is_authenticated:
            if usrProf in post.dislikes.all():
                post.dislikes.remove(usrProf)
            else:
                if usrProf in post.likes.all():
                    post.likes.remove(usrProf)
                post.dislikes.add(usrProf)
    return show_forum(request, forum_name_slug)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('meme_portal:logout'))

@login_required
def create_post(request,forum_name_slug):
    forum = get_object_or_404(Forum, slug=forum_name_slug)
    context_dict = {}

    if request.method=='POST' and request.user.is_authenticated:
        post_form=PostForm(request.POST)
        if post_form.is_valid():
            post=post_form.save(commit=False)
            user = get_object_or_404(UserProfile, user=request.user)
            post.forum=forum
            post.author=user
            post.save()
            return redirect(reverse('meme_portal:show_forum', kwargs={'forum_name_slug':forum_name_slug}))
    else:
        post_form=PostForm()

    context_dict['forum'] = forum
    context_dict['post_form'] = post_form
    return render(request, "meme_portal/create_post.html", context=context_dict)

@login_required
def create_page(request):
    context_dict = {}

    if request.method=='POST' and request.user.is_authenticated:
        forum_form=ForumForm(request.POST)
        if forum_form.is_valid():
            forum=forum_form.save(commit=False)
            user = get_object_or_404(UserProfile, user=request.user)
            forum.author=user
            forum.save()
            return redirect(reverse('meme_portal:show_forum', kwargs={'forum_name_slug':forum.slug}))
    else:
        forum_form=ForumForm()

    context_dict['forum_form'] = forum_form
    return render(request, "meme_portal/create_page.html", context=context_dict)

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "meme_portal/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="meme_portal/password/password_reset.html", context={"password_reset_form":password_reset_form})

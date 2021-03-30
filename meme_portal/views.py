from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm
from meme_portal.forms import UserForm, UserProfileForm, PostForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.generic.list import ListView
from meme_portal.models import Post, Forum, Comment
from datetime import datetime

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by the number of likes in descending order.
	# Retrieve the top 5 only -- or all if less than 5.
	# Place the list in our context_dict dictionary (with our boldmessage!)
	# that will be passed to the template engine.
	posts_list = Post.objects.order_by('-likes')[:5]
	context_dict = {}
	context_dict['post'] = posts_list

	forum_list = Forum.objects.order_by('?')[:5]
	context_dict = {}
	context_dict['forums'] = forum_list

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'meme_portal/index.html', context=context_dict)
	return response


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
	last_visit_cookie = get_server_side_cookie(request,
												'last_visit',
												str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7],
											'%Y-%m-%d %H:%M:%S')
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

def user_account(request):
	visitor_cookie_handler(request)

	return render(request, 'meme_portal/account.html')

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

@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return redirect(reverse('meme_portal:logout'))

@login_required
def create_post(request,forum_name_slug):
	try:
		forum = Forum.objects.get(slug=forum_name_slug)
	except Forum.DoesNotExist:
		forum=None

	if forum is None:
		return redirect('/forum/')

	form=PostForm()
	if request.method=='POST':
		form=PostForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.forum=forum
			user=UserProfile.objects.get(user=user)
			post.author=user
			post.save()
			return redirect(reverse('meme_portal:forum',
									kwargs={'forum_name_slug':forum_name_slug}))
	else:
		return render(request, "meme_portal/create_post.html",{'form':form})

@login_required
def post(request,forum_name_slug):
	forum = Forum.objects.get(slug=forum_name_slug)
	comments=Comment.objects.filter(post=post)
	post.name=name
	post.img_url=img_url
	post.time_posted=time_posted
	post.likes=likes
	author=UserProfile.objects.get(user=author)
	post.author=user_profile
	context_dict={'forum':forum, 'name':name, 'img_url':imr_url, 'time_posted':time_posted, 'likes':likes, 'author':author}
	return render(request,'meme_portal/create_post.html', context=context_dict)

@login_required
def create_page(request):
	return render(request,"meme_portal/create_page.html")

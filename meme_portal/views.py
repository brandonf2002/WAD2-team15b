from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm

def index(request):
    return render(request, 'meme_portal/index.html')
  
@login_required  
def create_page(request, category_name_slug):
    return render(request, 'meme_portal/create.html')
    
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
    return render(request, 'meme_portal/login.html')
    
def user_account(request):
    return render(request, 'meme_portal/account.html')
    
def create(request):
    return render(request, 'meme_portal/create.html')

def forum(request):
    return render(request, 'meme_portal/forum.html')
	
@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('meme_portal/index.html'))


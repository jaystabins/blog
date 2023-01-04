from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm, UsersRegisterForm, UserForm, ProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
from blog.models import Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.conf import settings

def login_view(request):
	form = UsersLoginForm(request.POST or None)
	if form.is_valid():
		next = request.GET.get('next')
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username = username, password = password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/")
	return render(request, "accounts/form.html", {
		"form" : form,
		"title" : "Login",
	})

@login_required
def register_view(request):
	form = UsersRegisterForm(request.POST or None)
	if form.is_valid():
		next = request.GET.get('next')
		user = form.save()
		password = form.cleaned_data.get("password")	
		user.set_password(password)
		user.save()
		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect("/")
	return render(request, "accounts/form.html", {
		"title" : "Register",
		"form" : form,
	})
 
def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")


@login_required
def edit_profile(request):
	user = User.objects.get(id=request.user.id)
	profile = Profile.objects.get(user=user)

	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=user)
		profile_form=ProfileForm(request.POST, request.FILES, instance=profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('article-list')
		return HttpResponse("HTTP 505 Error", status=505)
	else:
		profile_form = ProfileForm(instance=profile)
		user_form = UserForm(instance=user)
		context = {
			'profile_form': profile_form,
			'user_form': user_form,
		}
	return render(request, 'accounts/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('article-list')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        try:
            validate_email(email)
        except ValidationError:
            print('validation error')
            return render(request, 'accounts/contact_form.html', {'error': 'Invalid email address'})

        send_mail(
            'Message from Contact Form on Blog',
            name +'The following email sent you a message on your blog: [' + email + '] \n' + message,
            settings.EMAIL_HOST_USER,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        response = HttpResponse()
        response['HX-Trigger'] = 'close_modal'
        return response

    return render(request, 'accounts/contact_form.html')

def contact_success(request):
    return render(request, 'accounts/contact_success.html')

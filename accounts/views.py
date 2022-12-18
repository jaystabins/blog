from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm, UsersRegisterForm
from django.http import HttpResponseRedirect

from django.views.generic.base import View

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


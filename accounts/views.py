from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import UsersLoginForm


def login_view(request):
    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        next = request.GET.get("next")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(
        request,
        "accounts/form.html",
        {
            "form": form,
            "title": "Login",
        },
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        try:
            validate_email(email)
        except ValidationError:
            print("validation error")
            return render(
                request,
                "accounts/contact_form.html",
                {"error": "Invalid email address"},
            )

        send_mail(
            "Message from Contact Form on Blog",
            name
            + " sent the following email sent you a message on your blog: ["
            + email
            + "] \n"
            + message,
            settings.EMAIL_HOST_USER,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        response = HttpResponse()
        response["HX-Trigger"] = "close_modal"
        return response

    return render(request, "accounts/contact_form.html")

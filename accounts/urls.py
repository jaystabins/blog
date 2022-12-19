from django.urls import path
from .views import (
    login_view, register_view, logout_view, edit_profile, change_password
)

urlpatterns = [
    path("login/", login_view, name = "login"),
    path("register/", register_view, name = "register"),
    path('logout/', logout_view, name = "logout"),
    path('profile/profileupdate/', edit_profile, name = "profile-update"),
    path('profile/updatepassword/', change_password, name = "password-update"),
]
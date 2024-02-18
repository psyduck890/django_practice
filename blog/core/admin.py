from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm

class CustomeUserAdmin(UserAdmin):
    add_form = SignUpForm

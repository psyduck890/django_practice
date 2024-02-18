from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.views import PasswordResetDoneView
from django.template import RequestContext
from .forms import LoginForm, SignUpForm, QRCodeForm, ContactForm
from . import forms
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from qrcode import *
import qrcode.image.svg
from qrcode.image.pil import PilImage
from PIL import Image
import base64
from io import BytesIO
import time
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
import stripe


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def pricing(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    "price": "price_1Okj8OHew8paPTill2MqRi1h", # from Stripe
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url = request.build_absolute_uri(reverse("success")),
            cancel_url = request.build_absolute_uri(reverse("cancel")),
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'core/pricing.html')

def success(request):
    return render(request, 'core/success.html')

def cancel(request):
    return render(request, 'core/cancel.html')

@login_required
def dashboard(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.get('data', '')
        img = qrcode.make(data)
        img_name = 'qr' + str(time.time()) + '.png'
        img.save(str(settings.MEDIA_ROOT) + '/' + img_name)
        return render(request, 'core/dashboard.html', {'img_name': img_name})
    return render(request, 'core/dashboard.html')

def login(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                dj_login(request, user)
                message = f'Hello {user.username}! Welcome'
            else:
                message = 'Login failed'
    return render(request, 'core/login.html', context={'form': form, 'message': message})

def register(request):
    # form = UserCreationForm()
    form = SignUpForm()
    message = ''
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            message = f'You have successfully registered!'
            return redirect('../login/')
        else:
            message = 'Failed registration'
    context = {'form': form, 'message': message}
    return render(request, 'core/register.html', context=context)

def logout_user(request):
    logout(request)
    return render(request, 'core/home.html')

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Django enquiry'
            body = {
                'name': form.cleaned_data['Name'],
                'email': form.cleaned_data['Email'],
                'message': form.cleaned_data['Message']
            }
            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, 'bobbyesaev@gmail.com', ['crayfishconfessionists@gmail.com'])
            except:
                return HttpResponse('Invalid header')
            return redirect('/')
    return render(request, 'core/contact.html', {'form': form})

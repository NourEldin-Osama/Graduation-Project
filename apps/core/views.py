import datetime
import json

from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings as django_settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
print(f"LOCAL_IP: {django_settings.LOCAL_IP}")
DEFAULT_THEME = 'Light'
AVAILABLE_THEMES = ["Light", "Dark"]


def home(request):
    context = {"title": "Home"}
    return render(request, 'core/home.html', context)


def signup(request):
    context = {"title": "Sign Up"}
    return render(request, 'core/signup.html', context)


def login(request):
    context = {"title": "Login"}
    return render(request, 'core/login.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def profile(request):
    context = {"title": "Profile"}
    return render(request, 'core/profile.html', context)


@login_required
def settings(request):
    return None


@api_view(['POST'])
def get_theme(request):
    if 'Theme' not in request.COOKIES or request.COOKIES['Theme'] not in AVAILABLE_THEMES:
        response = Response({'theme_value': DEFAULT_THEME, 'first_time': 'Y'}, status=200)
        response.set_cookie(key='Theme', value=DEFAULT_THEME, max_age=datetime.timedelta(days=365))
        return response
    else:
        return Response({'theme_value': request.COOKIES['Theme'], 'first_time': 'N'}, status=200)


@api_view(['POST'])
def set_theme(request):
    # theme_value = request.POST.get("theme_value", DEFAULT_THEME)  # form-encoded data
    data = json.loads(request.body.decode("utf-8"))  # JSON-Encoded data
    theme_value = data.get('theme_value', DEFAULT_THEME)
    response = Response({'message': 'Success'}, status=200)
    if theme_value not in AVAILABLE_THEMES:
        theme_value = DEFAULT_THEME
    response.set_cookie(key='Theme', value=theme_value, max_age=datetime.timedelta(days=365))
    return response

import datetime

import requests
from django.conf import settings as django_settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User

# Create your views here.
print(f"Local Host: http://localhost:8000/")
print(f"Local Host: http://127.0.0.1:8000/")
print(f"Local Network IP: http://{django_settings.LOCAL_IP}:8000/")
DEFAULT_DESIGN_MODE = "Red_Dragon"
AVAILABLE_DESIGN_MODES = ["Red_Dragon", "Blue_Diamond", "Lavender_Love"]
CONTACT_EMAIL = django_settings.CONTACT_EMAIL
CONTACT_PHONE = django_settings.CONTACT_PHONE


def anonymous_required(function=None, redirect_url=None):
    """
    Decorator for views that checks that the user isn't logged in, redirecting
    to the home page if necessary.
    """
    if not redirect_url:
        redirect_url = django_settings.LOGIN_REDIRECT_URL
    actual_decorator = user_passes_test(lambda u: u.is_anonymous, login_url=redirect_url)

    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required
def signup(request):
    context = {"title": "Sign Up"}
    if request.method == "POST":
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:
            messages.error(request, "Password and Confirm Password doesn't match")
            return redirect('signup')

        username = request.POST.get("username", "")
        email = request.POST.get("email", "")

        # check if username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(username=email).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        elif User.objects.filter(email=email).exists() or User.objects.filter(email=username).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        # get user data
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        phone_number = request.POST.get("phone_number", "")
        gender = request.POST.get("gender", "")
        country = request.POST.get("country", "")
        city = request.POST.get("city", "")
        birthdate = request.POST.get("birthdate", "")

        # convert birthdate to YYYY-MM-DD format
        try:
            birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            birthdate = datetime.datetime.strptime(birthdate, "%d-%b-%Y").strftime("%Y-%m-%d")

        # create user
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name, phone=phone_number,
                                        gender=gender, country=country, city=city, birthdate=birthdate)

        # save profile picture
        picture = request.FILES.get("picture", False)
        if picture:
            user.picture = picture
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'core/signup.html', context)


@anonymous_required
def login(request):
    context = {"title": "Login", 'SOCIAL_MICROSOFT_PREMIUM': django_settings.SOCIAL_MICROSOFT_PREMIUM,
               'SOCIAL_LINKEDIN_PREMIUM': django_settings.SOCIAL_LINKEDIN_PREMIUM}
    if request.method == "POST":
        username_email = request.POST.get("username_email", "")
        password = request.POST.get("password", "")

        # check if user with username or email exists
        user = auth.authenticate(
            username=username_email,
            password=password
        ) or auth.authenticate(
            email=username_email,
            password=password
        )
        if user:
            # login user and redirect to home page
            auth.login(request, user)
            messages.success(request, f"Logged in successfully")
            return redirect('home')

        # if user doesn't exist, show error message
        messages.error(request, "Invalid username/email or password")
        return redirect('login')

    return render(request, 'core/login.html', context)


def home(request):
    context = {"title": "Home", "contact_email": CONTACT_EMAIL, "contact_phone": CONTACT_PHONE}
    return render(request, 'core/home.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def profile(request):
    context = {"title": "Profile"}
    return render(request, 'core/profile.html', context)


@login_required
def settings(request, template="personal_information"):
    context = {"title": "Settings", 'SOCIAL_MICROSOFT_PREMIUM': django_settings.SOCIAL_MICROSOFT_PREMIUM,
               'SOCIAL_LINKEDIN_PREMIUM': django_settings.SOCIAL_LINKEDIN_PREMIUM}
    root = "core/settings/"
    if template == "personal_information":
        context['template'] = root + "personal_information.html"
    elif template == "login_management":
        context['template'] = root + "login_management.html"
    elif template == "account_management":
        context['template'] = root + "account_management.html"
    elif template == "design_and_mode":
        context['template'] = root + "design_mode.html"
    elif template == "privacy_policy":
        context['template'] = root + "privacy_policy.html"
    elif template == "language":
        context['template'] = root + "language.html"
    else:
        context['template'] = root + "personal_information.html"
    return render(request, 'core/settings/settings.html', context)


@api_view(['POST'])
def get_design_mode(request):
    """
    This function retrieves the current design mode from a cookie in the request,
    or sets a default value if it is not present or invalid.
    It returns a JSON response with the current design mode and a flag
    indicating whether it is the first time the user has accessed the page.
    If it is the first time, it sets a cookie with the design mode value that will expire in one year.
    """
    if 'design_mode' not in request.COOKIES or request.COOKIES['design_mode'] not in AVAILABLE_DESIGN_MODES:
        design_mode = DEFAULT_DESIGN_MODE
        first_time = 'Y'
    else:
        design_mode = request.COOKIES.get('design_mode', DEFAULT_DESIGN_MODE)
        first_time = 'N'
    response = Response({'design_mode': design_mode, 'first_time': first_time, }, status=200)
    if first_time == "Y":
        response.set_cookie(
            key='design_mode',
            value=design_mode,
            max_age=datetime.timedelta(days=365)
        )
    return response


@api_view(['POST'])
def set_design_mode(request):
    """
    This function set the design mode of the website.
    It retrieves the design mode value from the request body,
    sets it to the default value if not provided, and ensures that it has a proper title case format.
    It then sets a cookie with the design mode value
    and returns a response object with a success message and the design mode value.
    """
    design_mode = request.data.get('design_mode', DEFAULT_DESIGN_MODE).strip().title()
    design_mode = design_mode if design_mode in AVAILABLE_DESIGN_MODES else DEFAULT_DESIGN_MODE
    response = Response({
        'message': 'Success',
        'design_mode': design_mode,
    }, status=200)
    response.set_cookie(
        key='design_mode',
        value=design_mode,
        max_age=datetime.timedelta(days=365)
    )
    return response


@api_view(['POST'])
def update_personal_info(request):
    """
    This function updates the user's profile information.
    It retrieves the user's information from the request body,
    and updates the user's information in the database.
    """
    data = request.data
    user = request.user
    print(data)
    print(user)
    # user.first_name = data.get('first_name', user.first_name) or user.first_name
    # user.last_name = data.get('last_name', user.last_name) or user.last_name
    # user.username = data.get('username', user.username) or user.username
    # user.email = data.get('email', user.email) or user.email
    # user.phone = data.get('phone', user.phone) or user.phone
    # user.country = data.get('country', user.country) or user.country
    # user.city = data.get('city', user.city) or user.city
    # user.birthdate = data.get('birthdate', user.birthdate) or user.birthdate
    # user.gender = data.get('gender', user.gender) or user.gender
    return Response({'message': 'Success'}, status=200)


@api_view(['POST'])
def facial_login(request):
    frame = request.POST.get('image')
    payload = {'image': frame}
    r = requests.post("https://facialauthentication.pythonanywhere.com/recognize_user", data=payload)
    if r.status_code == 200 and r.json()['username'] != "":
        u = User.objects.get(username=r.json()['username'])
        auth.login(request, u, backend='django.contrib.auth.backends.ModelBackend')
        return Response({'result': "Done"}, status=200)
    return Response({'result': "Fail"}, status=200)


@api_view(['POST'])
def enable_facial_login(request):
    frame = request.POST.get('image')
    payload = {'image': frame, 'username': request.user.username}
    r = requests.post("https://facialauthentication.pythonanywhere.com/add_user", data=payload)
    if r.status_code == 200:
        request.user.facial_login = True
        request.user.save()
        return Response({'result': "Done"}, status=200)
    return Response({'result': "Fail"}, status=200)


def health_check(request):
    return HttpResponse("OK", status=200)

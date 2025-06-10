from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import UserProfile, ShortenedUrl
import uuid
import time
from datetime import datetime
from django.utils.timezone import make_aware

#* ===== ACCOUNT SYSTEM ===== *#

def Register(request):

    if request.method == "POST":
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")

        if User.objects.filter(username = username).exists():
            return render(request, "accounts/register.html", {"error": "Username is already taken! Please use a different one."})
        
        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {"error": "This email is already in use. Please use a different one."})
        
        user = User.objects.create_user(username= username, password= password, email= email)
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('dashboard')
    
    return render(request, "accounts/register.html")

def Login(request):
    if request.method == "POST":
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")

        user = authenticate(request, password = password, email = email, username = username)

        try:
            User.objects.get(username=username)
        except:
            return render(request, "Login.html", {"error":"Profile with that username does not exist!"})
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, "accounts/register.html", {"error": "Invalid creditentials!"})

    return render(request, "accounts/login.html")

@login_required
def DeleteAccount(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect('home') 
    
    return render(request, "delete_account.html")

@login_required
def AccountDetail(request):
    context = {
        "username": request.user.username,
        "email": request.user.email
    }
    return render(request, "accounts/account.html", context)

#* ===== MISCCELLANEOUS ===== *#

def Home(request):
    return render(request, "misc/index.html")

def Redirect(request):
    return redirect("home")

#* ===== DASHBOARD =====*#

@login_required
def Dashboard(request):
    return render(request, "app/dashboard.html")

#* ====== URL SHORTENING &  URL STUFF ===== *#

def ShortenUrl(request):
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        custom_alias = request.POST.get("custom_alias")
        expiry_date_str = request.POST.get("expiry_date") # 14:25 25/06/2025
        active_status = request.POST.get("active")
        max_uses_str = request.POST.get("max_uses")
        url_password = request.POST.get("url_password")

        hashed_url_password = make_password(url_password) if url_password else None
        short_code = str(uuid.uuid4())[:20]

        expiry_date = None
        if expiry_date_str:
            try:
                # *** CHANGE THE FORMAT STRING HERE ***
                expiry_date = datetime.strptime(expiry_date_str, '%H:%M %d/%m/%Y')
                expiry_date = make_aware(expiry_date)
            except ValueError:
                messages.error(request, "Invalid expiry date format. Please use **HH:MM DD/MM/YYYY**.")
                return render(request, "app/url_create.html", {
                    "original_url": original_url,
                    "custom_alias": custom_alias,
                    "max_uses_str": max_uses_str,
                    "active_status": active_status,
                    "expiry_date_str": expiry_date_str,
                })

        max_uses = None
        if max_uses_str:
            try:
                max_uses = int(max_uses_str)
            except ValueError:
                messages.error(request, "Max uses must be a valid number.")
                return render(request, "app/url_create.html", {
                    "original_url": original_url,
                    "custom_alias": custom_alias,
                    "expiry_date_str": expiry_date_str,
                    "active_status": active_status,
                    "max_uses_str": max_uses_str,
                })

        is_active = True if active_status == 'on' else False

        current_user = request.user if request.user.is_authenticated else None

        try:
            ShortenedUrl.objects.create(
                original_url=original_url,
                short_code=short_code,
                owner=current_user,
                custom_code=custom_alias if custom_alias else None,
                expiry_date=expiry_date,
                max_uses=max_uses,
                url_password=hashed_url_password,
                is_active=is_active
            )
            messages.success(request, "Shortened URL successfully! You will be redirected to the dashboard shortly.")
            return render(request, 'app/url_create.html', {'redirect_to_dashboard': True})

        except Exception as e:
            messages.error(request, "Something went wrong! Please try again or choose a different custom alias if one was provided.")
            return render(request, 'app/url_create.html', {
                "original_url": original_url,
                "custom_alias": custom_alias,
                "expiry_date_str": expiry_date_str,
                "max_uses_str": max_uses_str,
                "active_status": active_status,
            })

    return render(request, 'app/url_create.html')

"""
'DIRS': [
            'templates/',
        ],
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import UserProfile, ShortenedUrl
from django.shortcuts import get_object_or_404
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
    link = ShortenedUrl.objects.all()
    return render(request, "app/dashboard.html", {"link": link})

#* ====== URL SHORTENING &  URL STUFF ===== *#

def ShortenUrl(request):
    if request.method == "POST":
        original_url = request.POST.get("original_url", "").strip()
        custom_alias = request.POST.get("custom_alias", "").strip()
        expiry_date_str = request.POST.get("expiry_date", "").strip()  # HH:MM DD/MM/YYYY
        active_status = request.POST.get("active")
        max_uses_str = request.POST.get("max_uses", "").strip()
        url_password = request.POST.get("url_password", "").strip()
        provided_length = request.POST.get('length')

        hashed_url_password = make_password(url_password) if url_password else None
        expiry_date = None
        if expiry_date_str:
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%H:%M %d/%m/%Y')
                expiry_date = make_aware(expiry_date)
            except ValueError:
                return render(request, "app/url_create.html", {
                    "original_url": original_url,
                    "custom_alias": custom_alias,
                    "expiry_date_str": expiry_date_str,
                    "max_uses_str": max_uses_str,
                    "active_status": active_status,
                    "error": "Invalid expiry date format. Please use HH:MM DD/MM/YYYY"
                })

        max_uses = None
        if max_uses_str:
            try:
                max_uses = int(max_uses_str)
                if max_uses < 1:
                    raise ValueError
            except ValueError:
                return render(request, "app/url_create.html", {
                    "original_url": original_url,
                    "custom_alias": custom_alias,
                    "expiry_date_str": expiry_date_str,
                    "max_uses_str": max_uses_str,
                    "active_status": active_status,
                    "error": "Max uses must be a positive number!"
                })

        is_active = True if active_status == 'on' else False

        current_user = request.user if request.user.is_authenticated else None

        if provided_length == None:
            provided_length = 20
        else:
            pass

        if custom_alias:
            if ShortenedUrl.objects.filter(custom_code=custom_alias).exists():
                return render(request, "app/url_create.html", {
                    "original_url": original_url,
                    "custom_alias": custom_alias,
                    "expiry_date_str": expiry_date_str,
                    "max_uses_str": max_uses_str,
                    "active_status": active_status,
                    "error": "The provided alias is already in use! Please choose another one."
                })
            short_code = custom_alias
        else:
            while True:
                random_code = str(uuid.uuid4())[:provided_length]
                if not ShortenedUrl.objects.filter(short_code=random_code).exists():
                    short_code = random_code
                    break
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
            print("Shortened URL created successfully:", short_code)
            return redirect('dashboard')

        except Exception as e:
            print("Error creating ShortenedUrl:", e)
            return render(request, 'app/url_create.html', {
                "original_url": original_url,
                "custom_alias": custom_alias,
                "expiry_date_str": expiry_date_str,
                "max_uses_str": max_uses_str,
                "active_status": active_status,
                "error": "Something went wrong! Please, try again!"
            })
        
    return render(request, 'app/url_create.html', {
        "original_url": "",
        "custom_alias": "",
        "expiry_date_str": "",
        "max_uses_str": "",
        "active_status": "",
        "error": ""
    })


def DeleteURL(request, pk):
    links = get_object_or_404(ShortenedUrl, pk = pk)
    return render(request, 'app/url_delete.html', {"links": links})
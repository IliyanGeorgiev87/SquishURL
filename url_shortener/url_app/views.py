from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import UserProfile, ShortenedUrl
import uuid
from datetime import datetime

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

    return render(request, "login.html")

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
        expiry_date = request.POST.get("expiry_date")
        active = request.POST.get("active")
        max_uses = request.POST.get("max_uses")
        url_password = request.POST.get("url_password")
        
        hashed_url_password = make_password(url_password)
        short_code = str(uuid.uuid4())[:20]

        ShortenedUrl.objects.create(
            original_url = original_url,
            short_code = short_code,
            created_at = datetime.now,
            url_password = hashed_url_password,
            is_active = active
        )


        """
        def add(request):
        if request.method == "POST":
            link = request.POST['link']
            link_id = str(uuid.uuid4())[:5]
            new_link = LinkInfo(link=link, link_id=link_id)
            new_link.save()

        return HttpResponse(link_id)
        """

    return render(request, 'app/url_create.html')

"""
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=20, unique=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    custom_code = models.CharField(max_length=20, unique=True, null=True, blank=False)
    expiry_date = models.DateTimeField()
    max_uses = models.IntegerField(null=True, blank=True)
    current_uses = models.IntegerField(default=0)
    url_password  = models.CharField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=True)
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import UserProfile

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
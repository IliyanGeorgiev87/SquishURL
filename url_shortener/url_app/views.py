from django.shortcuts import render, redirect

#* ===== ACCOUNT SYSTEM ===== *#
#* ===== MISCCELLANEOUS ===== *#
def Home(request):
    return render(request, "misc/index.html")
def Redirect(request):
    return redirect("home")
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import IncUser
from django.contrib import messages

# def user_register(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#         password1 = request.POST["password1"]
#         password2 = request.POST["password2"]

#         if password1 != password2:
#             messages.error(request, "Password tidak cocok.")
#             return redirect("register")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username sudah digunakan.")
#             return redirect("register")

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email sudah digunakan.")
#             return redirect("register")

#         user = User.objects.create_user(username=username, email=email, password=password1)
#         user.save()
#         login(request, user)
#         return redirect("complaint_list") 

#     return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        nik = request.POST["nik"]
        password = request.POST["password"]
        print(nik)
        print(password)
        user = authenticate(request, username=nik, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("complaint_list") 
        else:
            messages.error(request, "Username atau password salah.")
            return redirect("login")

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect("login")
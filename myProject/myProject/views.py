from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from myApp.models import customUser
from django.contrib import messages
from django.contrib import messages
from myApp import EmailBackEnd
from django.contrib.auth import login as auth_login

def signupPage(request):
    error_messages = {
        'password_error': 'Password and Confirm Password not match',
    }
    if request.method == "POST":
        uname = request.POST.get("name")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirmpasword")

        if pass1 != pass2:
             messages.error(request, error_messages['password_error'])
        else:
            # Use your customUser model to create a user
            myuser = customUser.objects.create_user(username=uname, email=email, password=pass1)
            myuser.save()
            return redirect("loginPage")

    # messages.success(request, 'Signup successful.')
    return render(request, "signup.html")


def loginPage(request):
    error_messages = {
        'username_error': 'Username is required.',
        'password_error': 'Password is required.',
        'login_error': 'Invalid username or password. Please try again.',
    }

    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("password")
        
        if not username:
            messages.error(request, error_messages['username_error'])
        elif not pass1:
            messages.error(request, error_messages['password_error'])
        else:
            user = EmailBackEnd.authenticate(request, username=username, password=pass1,)

            if user is not None:
                login(request,user)
                user_type = user.user_type
                if user_type == '1':
                    return redirect("adminPage")
                elif user_type == '2':
                    return render(request, "Staff/staffhome.html")
                elif user_type == '3':
                    return render(request, "Stustudenthome.html")
                else:
                    return redirect("signupPage")
            else:
                messages.error(request, error_messages['login_error'])

    return render(request, "login.html")

def adminPage(request):
    
    return render(request,"myAdmin/adminhome.html")


def home(request):
    return render(request, 'home.html') 


def myProfile(request):
    user = request.user  # You can directly access the authenticated user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)
 
def profileUpdate(request):
    error_messages = {
        'success': 'Profile Update Successfully',
        'error': 'Profile Not Updated'
    }
    
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        print(profile_pic,username,firstname,lastname,email,password)
        try:
            cuser = customUser.objects.get(id=request.user.id)
            
            cuser.first_name = firstname
            cuser.last_name = lastname
            cuser.profile_pic = profile_pic
            
            if password is not None and password != "":
                cuser.set_password(password)
            if profile_pic is not None and profile_pic != "":
                cuser.profile_pic = profile_pic
            cuser.save()
            auth_login(request, cuser)
            messages.success(request, error_messages['success'])
            return redirect("profileUpdate")
        except:
            messages.error(request, error_messages['error'])
    
    return render(request, 'profile.html')

def logoutPage(request):
    logout(request)
    
    return redirect("loginPage")
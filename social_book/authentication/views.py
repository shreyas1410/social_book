from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):

    return render(request, 'index.html')

def signup(request):

    if request.method=="POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.firstname = fname
        myuser.lastname = lname

        myuser.save()
        messages.success(request, "Account created Successfully!!")
        return redirect('signin')

    return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(username=username, password = pass1 )

        if user is not None:
            login(request, user)
            fname = user.first_name
            # return render(request, "userlist.html", {"fname":fname})
            return redirect('user_list')
        else:
            messages.error(request, "Unable to Sign-in")
            return redirect('home')

    return render(request, 'signin.html')

def user_list(request):
    users= User.objects.all()
    print(users)
    return render (request, "userlist.html",{"users":users})

def signout(request):
    logout(request)
    return redirect('home')

#def register(request):
    #return render(request,'signup.html')

#  def login(request):
    #return render(request,'signin.html')
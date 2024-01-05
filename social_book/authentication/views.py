from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login, logout, get_user_model

CustomUser = get_user_model()
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
        # print(username,fname,lname,email,pass1)
        CustomUser = get_user_model()
        myuser = CustomUser.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        print(myuser)
        myuser.save()
        messages.success(request, "Account created Successfully!!")
        return redirect('signin1')

    return render(request, 'signup1.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST.get('email')
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

    return render(request, 'signin1.html')

def user_list(request):
        
    CustomUser = get_user_model()
    # users= CustomUser.objects.all()
    # print(users)
    # return render (request, "userlist.html",{"users":users})
    users = CustomUser.objects.filter(public_visibility=True)
    return render(request, 'userlist.html', {'users': users})


def signout(request):
    logout(request)
    return redirect('home')

#def register(request):
    #return render(request,'signup.html')

#  def login(request):
    #return render(request,'signin.html')
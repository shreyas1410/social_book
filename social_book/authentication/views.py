from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import UploadedFile

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
        public_visibility= request.POST.get('public_visibility')
        
        if public_visibility =='on':
            public_visibility = True
        else:
            public_visibility = False
        # print(public_visibility)
        # print(username,fname,lname,email,pass1)
        CustomUser = get_user_model()
        myuser = CustomUser.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.public_visibility = public_visibility
        # print(myuser)
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

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            messages.success(request, 'Book uploaded successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Error uploading the book. Please check the form.')
    else:
        form = FileUploadForm()

    return render(request, 'upload_files.html', {'form': form})

@login_required
def uploaded_images(request):
    user_files = UploadedFile.objects.filter(user = request.user)
    return render(request, 'uploaded_files.html', {'user_files':user_files})
    # return render(request, 'userlist.html', {'users': users})                                                

#def register(request):
    #return render(request,'signup.html')

#  def login(request):
    #return render(request,'signin.html')
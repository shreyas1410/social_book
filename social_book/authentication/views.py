from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from .forms import FileUploadForm
from .models import UploadedFile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,UploadedFileSerializer
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import views as auth_views

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
class GenerateToken(APIView):
    def post(self, request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')

            #print(f"Received credentials: email={email}, password={password}")

            user = authenticate(request, username=username, password=password)

            #print(f"Authenticated user: {user}")

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token})
            else:
                return Response({'error': 'Invalid Credentials'}, status=401)
        return Response({'error': 'Invalid request method'}, status=400)                                       

#def register(request):
    #return render(request,'signup.html')

#  def login(request):
    #return render(request,'signin.html')

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

class CustomUserDetailView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the logged-in user
        return self.request.user
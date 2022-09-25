from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

import hashlib, uuid

from account.models import User
from .forms import UserLoginForm, UserRegisterForm

def createHashedPassword(email, username, password):
    # create salt for passwords
    salt = "salt1" + email + "salt2" + username + "salt3"
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password

# Create your views here.
class LoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['username']
            passwordEntered = form.cleaned_data['password']

            # get user from the database
            user = get_object_or_404(User,username=userName)
            hashedPassword = createHashedPassword(user.email, user.username, passwordEntered)

            if hashedPassword == user.password_hash:          
                # add user login log to the database (task)
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("password-wrong")

        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            userName = form.cleaned_data['username']
            passwordEntered = form.cleaned_data['password']
            hashedPassword = createHashedPassword(email, userName, passwordEntered)
            
            # check are there any username or email same
            usersByUsername = User.objects.filter(username=userName)
            usersByEmail = User.objects.filter(email=email)
            if usersByUsername.count() == 0 and usersByEmail.count() == 0:
                # create process 
                newUser = form.save(commit=False)
                newUser.password_hash = hashedPassword
                newUser.save()
                return HttpResponseRedirect("/")
            return HttpResponse("there is a user")

        return render(request, self.template_name, {'form': form})

def profile(request):
    return render(request, 'account/profile.html')
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

import hashlib, uuid

from account.models import User
from .forms import UserLoginForm

def createHashedPassword(email, username, password):
    # create salt for passwords
    salt = uuid.uuid4().hex + email + uuid.uuid4().hex + username + uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
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

def register(request):
    return render(request, 'account/register.html')

def profile(request):
    return render(request, 'account/profile.html')
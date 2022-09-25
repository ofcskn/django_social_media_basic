from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import User
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
class LoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                # No backend authenticated the credentials
                return HttpResponse("wrong")


        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            userName = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # check are there any username or email same
            usersByUsername = User.objects.filter(username=userName)
            usersByEmail = User.objects.filter(email=email)
            if usersByUsername.count() == 0 and usersByEmail.count() == 0:
                # create process 
                user = form.save()
                user.set_password(password)
                user.save()
                return HttpResponseRedirect("/")
            return HttpResponse("there is a user")

        return render(request, self.template_name, {'form': form})

@login_required
def profile(request):
    return render(request, 'account/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import User, UserFollower
from .forms import ProfileAvatarUploadForm, ProfileChangePasswordForm, ProfileEditForm, UserLoginForm, UserRegisterForm
from django.urls import reverse

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
                print("save")
                # create process 
                user = form.save()
                user.set_password(password)
                user.save()
                return HttpResponseRedirect("/")
            return HttpResponse("there is a user")

        return render(request, self.template_name, {'form': form})

class ProfileEditView(View):
    form_class = ProfileEditForm
    template_name = 'account/profile/edit.html'
    def get(self, request):
        current_user = request.user
        return render(request, self.template_name, {"data": current_user})
    def post(self, request):
        current_user = request.user
        form = self.form_class(request.POST, instance=current_user)
        if form.is_valid():
            print(form.cleaned_data['about_me'])
            email = form.cleaned_data['email']
            userName = form.cleaned_data['username']
            # check are there any username or email same
            usersByUsername = User.objects.filter(username=userName).exclude(pk=current_user.pk)
            usersByEmail = User.objects.filter(email=email).exclude(pk=current_user.pk)
            if usersByUsername.count() == 0 and usersByEmail.count() == 0:  
                # update process 
                form.save()
            else:
                return HttpResponse("there is a user")
        return render(request, self.template_name, {'data': current_user})

class ProfileChangePasswordView(View):
    form_class = ProfileChangePasswordForm
    template_name = 'account/profile/change_password.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        current_user = User.objects.get(pk=request.user.pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            passwordOld = form.cleaned_data['old_password']
            password = form.cleaned_data['password']
            passwordRepeat = form.cleaned_data['password_repeat']

            if request.user.check_password(passwordOld):
                if passwordRepeat == password:
                    # create new password
                    current_user.set_password(password)
                    current_user.save()
                else:
                    return HttpResponse("your-password-not-equal")
            else:
                print("old-password-wrong")
                return HttpResponse("old-password-wrong")

        return render(request, self.template_name)

class ProfileAvatarUploadView(View):
    form_class = ProfileAvatarUploadForm
    def post(self, request):
        logged_user = User.objects.get(pk=request.user.pk)
        form = self.form_class(request.POST, request.FILES, instance=logged_user)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect(reverse('core:get_user', args=(request.user.username,)))
        else:
            return HttpResponse("not-valid")


@login_required()
def following_requests(request):
    # get all requests by the logged user
    data = UserFollower.objects.filter(to=request.user).order_by("-date")
    return render(request, 'account/profile/following_requests.html', {"data": data})

@login_required()
def accept_following_request(request, id):
    if request.method == "POST":
        current_user = request.user
        # get Userfollower by the logged user
        userFollower = get_object_or_404(UserFollower,pk=id)
        # check the folowing request is for current_user
        if userFollower.to == current_user:
            userAcceptStatus = userFollower.is_accepted != True
            # update is_acccepted by filtering
            UserFollower.objects.filter(pk=id, to=current_user).update(is_accepted=userAcceptStatus)
            return HttpResponse(f"{userAcceptStatus}")
        else:
            return HttpResponse("bad-request")
    else:
        return HttpResponse('you need to post')

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import User, UserFollower
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

@login_required()
def profile(request):
    return render(request, 'account/profile.html')


@login_required()
def change_password(request):
    return HttpResponse('reset pass')


@login_required()
def following_requests(request):
    # get all requests by the logged user
    data = UserFollower.objects.filter(to=request.user).order_by("-date")
    return render(request, 'account/profile/following_requests.html', {"data": data})

@login_required()
def accept_following_request(request, id):
    print("id", id)
    if request.method == "POST":
        current_user = request.user
        # get Userfollower by the logged user
        userFollower = get_object_or_404(UserFollower,pk=id)
        # check the folowing request is for current_user
        if userFollower.to == current_user:
            # update is_acccepted by filtering
            UserFollower.objects.filter(pk=id, is_accepted=False, to=current_user).update(is_accepted=True)
            return HttpResponse("success")
        else:
            return HttpResponse("bad-request")
    else:
        return HttpResponse('you need to post')

from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .forms import UserForm

# Create your views here.
class LoginView(View):
    template_name = 'account/login.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        print(self)
        form = self.form_class(request.POST)
        if form.is_valid():
            print("success", form)
            # <process form cleaned data>
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})

def register(request):
    return render(request, 'account/register.html')

def profile(request):
    return render(request, 'account/profile.html')
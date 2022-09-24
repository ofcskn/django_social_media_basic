from django.shortcuts import render
from django.views import View

# Create your views here.
class LoginView(View):
    template_name = 'account/login.html'
    def get(self, request):
        print('get_called')
        return render(request, self.template_name)
    def post(self, request):
        print('post_called')
        pass

def register(request):
    return render(request, 'account/register.html')

def profile(request):
    return render(request, 'account/profile.html')
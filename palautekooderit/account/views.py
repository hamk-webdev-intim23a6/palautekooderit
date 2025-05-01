from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from feedbacksystem.forms import CustomLoginForm
from feedbacksystem.forms import CustomSignupForm

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'
    
class SignUpView(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    

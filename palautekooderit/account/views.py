from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from feedbacksystem.forms import CustomLoginForm
from feedbacksystem.forms import CustomSignupForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'
    
class SignUpView(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        # Save the new user and log them in
        user = form.save()
        login(self.request, user)  # Log the user in automatically
        
        # Optionally, you can add a success message here
        messages.success(self.request, 'Account created and logged in successfully!')
        
        return redirect(self.success_url)  # Redirect to success_url
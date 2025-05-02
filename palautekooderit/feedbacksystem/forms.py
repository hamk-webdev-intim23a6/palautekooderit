# forms.py
from django import forms
from .models import Topic, Feedback
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# The form for submitting feedback
class FeedbackForm(forms.Form):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all().order_by('name'),
        label="Aihe",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-placeholder': 'Valitse aihe'
        })
    )
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        label="Arvostelu (1-5)",
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    positive = forms.CharField(
        label="Mikä oli positiivista? (Valinnainen)",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )
    negative = forms.CharField(
        label="Mitä voisi parantaa? (Valinnainen)",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )
    ideas = forms.CharField(
        label="Muita ideoita? (Valinnainen)",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )

# The form for creating a new topic
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
        labels = {
            'name': 'Aiheen nimi',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        
# This form is used in login 
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Käyttäjätunnus'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Salasana'
        })
    )

#This form is used in signup

class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control custom-width',
            'placeholder': 'Käyttäjätunnus'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control custom-width',
            'placeholder': 'Salasana'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control custom-width',
            'placeholder': 'Vahvista salasana'
        })
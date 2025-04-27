# forms.py
from django import forms
from .models import Topic, Feedback

# The form for submitting feedback
class FeedbackForm(forms.Form):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all().order_by('name'),
        label="Aihe",
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
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

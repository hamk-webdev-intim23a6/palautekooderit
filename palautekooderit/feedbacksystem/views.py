from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback, Topic
from .forms import TopicForm
from .forms import Topic

# Allows selection of feedback item
def home(request):
    topic_form = TopicForm()
    return render(request, 'home.html', {'topic_form': topic_form})

#Allows giving feedback
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            topic_instance = topic_form.cleaned_data['name']
            try:
                rating = int(request.POST.get('rating'))
                positive = request.POST.get('positive', '')
                negative = request.POST.get('negative', '')
                ideas = request.POST.get('ideas', '')

                feedback = Feedback(
                    topic=topic_instance,
                    user=request.user,
                    rating=rating,
                    positive=positive,
                    negative=negative,
                    ideas=ideas
                )
                feedback.save()

                messages.success(request, 'Feedback sent.')
                return redirect('home')
            except ValueError:
                error_message = "Please enter a valid rating between 1 and 5."
                return render(request, 'home.html', {'topic_form': topic_form, 'error': error_message})
        else:
            return render(request, 'home.html', {'topic_form': topic_form, 'form_errors': topic_form.errors})
    else:
        return redirect('home')

#Allows creation of feedback items    
def topic(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TopicForm()
    return render(request, 'administration/topic.html', {'form': form, 'topics': topics})

#Allows viewing of analytics
def analytics(request):
    return HttpResponse("See analytics")

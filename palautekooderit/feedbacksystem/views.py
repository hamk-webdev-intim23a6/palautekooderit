from django.http import HttpResponse
from django.shortcuts import render
from .forms import TopicForm
from .forms import Topic

# Allows selection of feedback item
def home(request):
    return HttpResponse("Select Feedback-item")

#Allows giving feedback
def submit_feedback(request):
    return HttpResponse("Submit Feedback")

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

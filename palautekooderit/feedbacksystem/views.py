from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback, Topic
from .forms import FeedbackForm, TopicForm
from django.contrib import messages
from django.db.models import Avg, Count

# Home page view - displays the feedback form
def home(request):
    form = FeedbackForm()
    return render(request, 'home.html', {'form': form})

# Handles feedback submission
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        
        if form.is_valid():
            topic_instance = form.cleaned_data['topic']
            rating = form.cleaned_data['rating']
            positive = form.cleaned_data['positive']
            negative = form.cleaned_data['negative']
            ideas = form.cleaned_data['ideas']

            Feedback.objects.create(
                topic=topic_instance,
                user=request.user,
                rating=rating,
                positive=positive,
                negative=negative,
                ideas=ideas
            )

            messages.success(request, 'Kiitos palautteesta!')

            return redirect('home')
        else:
            messages.error(request, 'Tarkista lomakkeen virheet ja yritä uudelleen.')
            return render(request, 'home.html', {'form': form})
    else:
        return redirect('home')

# Allows creation of feedback items (Topics)
def topic(request):
    topics = Topic.objects.all().order_by('name')
    if request.method == 'POST':
        topic_creation_form = TopicForm(request.POST)
        if topic_creation_form.is_valid():
            new_topic = topic_creation_form.save()
            messages.success(request, f"Aihe '{new_topic.name}' luotu onnistuneesti.")
            return redirect('topic')
        else:
            messages.error(request, 'Aiheen luominen epäonnistui. Tarkista virheet.')
    else:
        topic_creation_form = TopicForm()

    return render(request, 'administration/topic.html', {
        'form': topic_creation_form,
        'topics': topics
    })

#Allows viewing of analytics
def analytics(request):
    topics = Topic.objects.all()
    
    topic_data = []
    for topic in topics:
        feedbacks = Feedback.objects.filter(topic=topic)
        
        # Get average rating and feedback count
        avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']
        feedback_count = feedbacks.count()

        # Gather comments by category (positive, negative, ideas)
        positive_comments = [(feedback.user.username, feedback.positive) for feedback in feedbacks if feedback.positive]
        negative_comments = [(feedback.user.username, feedback.negative) for feedback in feedbacks if feedback.negative]
        ideas_comments = [(feedback.user.username, feedback.ideas) for feedback in feedbacks if feedback.ideas]
        
        topic_data.append({
            'topic': topic,
            'avg_rating': avg_rating,
            'feedback_count': feedback_count,
            'positive_comments': positive_comments,
            'negative_comments': negative_comments,
            'ideas_comments': ideas_comments,
        })

    return render(request, 'administration/analytics.html', {
        'topic_data': topic_data
    })
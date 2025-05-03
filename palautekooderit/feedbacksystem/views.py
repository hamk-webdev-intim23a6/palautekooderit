from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Feedback, Topic
from .forms import FeedbackForm, TopicForm
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.models import User
from django.shortcuts import render


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
            is_anonymous = form.cleaned_data.get('anonymous', False)

            feedback = Feedback(
                topic=topic_instance,
                rating=rating,
                positive=positive,
                negative=negative,
                ideas=ideas,
            )

            if not is_anonymous:
                feedback.user = request.user

            feedback.save()

            messages.success(request, 'Kiitos palautteesta!')

            return redirect('home')
        else:
            messages.error(request, 'Tarkista lomakkeen virheet ja yritä uudelleen.')
            return render(request, 'home.html', {'form': form})
    else:
        return redirect('home')
def user_is_staff(user):
    if user.is_staff:
        return True
    else:
        return False
# Allows creation of feedback items (Topics)
@user_passes_test(user_is_staff, login_url='home')
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

@user_passes_test(user_is_staff, login_url='home')
def analytics(request):
    topic_list = Topic.objects.all()
    user_list = User.objects.all()

    # Get selected user from GET parameter
    selected_user_id = request.GET.get('user')
    selected_user = None

    if selected_user_id:
        if selected_user_id == "None":
                feedbacks = Feedback.objects.filter(user=None)
        else:
            try:
                selected_user = User.objects.get(id=selected_user_id)
                if selected_user != None:
                    selected_user_id = selected_user.id
                feedbacks = Feedback.objects.filter(user=selected_user)
            except User.DoesNotExist:
                feedbacks = Feedback.objects.all()
    else:
        feedbacks = Feedback.objects.all()

    
    selected_topic_id = request.GET.get('topic')

    try:
        selectedTopic = topic_list.filter(id=selected_topic_id).first()
        if(selectedTopic != None):
            selected_topic_id = selectedTopic.id
            filteredTopics = [selectedTopic]
        else:
            filteredTopics = topic_list
    except: # I do not care if the error is unspecific; This ensures good function always. Pythons philosophy can go jump in a well. - Valtari
        filteredTopics = topic_list

    topic_data = []
    for topic in filteredTopics:
        topic_feedbacks = feedbacks.filter(topic=topic)

        ratings = [0,0,0,0,0]
        for feedback in topic_feedbacks:
            ratings[feedback.rating-1] += 1

        avg_rating = topic_feedbacks.aggregate(Avg('rating'))['rating__avg']
        feedback_count = topic_feedbacks.count()

        positive_comments = topic_feedbacks.values_list('user__username', 'positive')
        negative_comments = topic_feedbacks.values_list('user__username', 'negative')
        ideas_comments = topic_feedbacks.values_list('user__username', 'ideas')

        topic_data.append({
            'topic': topic,
            'avg_rating': avg_rating,
            'feedback_count': feedback_count,
            'positive_comments': positive_comments,
            'negative_comments': negative_comments,
            'ideas_comments': ideas_comments,
            'ratings': ratings,
        })

    return render(request, 'administration/analytics.html', {
        'topic_data': topic_data,
        'user_list': user_list,
        'selected_user_id': selected_user_id,
        'topic_list': topic_list,
        'selected_topic_id': selected_topic_id,
    })
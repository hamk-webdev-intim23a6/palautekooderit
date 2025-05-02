from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('submit/', views.submit_feedback, name='submit_feedback'),
    path('topic/', views.topic, name='topic'),
    path('analytics/', views.analytics, name='analytics')
]
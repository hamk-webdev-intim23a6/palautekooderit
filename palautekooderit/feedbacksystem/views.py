from django.http import HttpResponse

# Allows selection of feedback item
def home(request):
    return HttpResponse("Select Feedback-item")

#Allows giving feedback
def submit_feedback(request):
    return HttpResponse("Submit Feedback")

#Allows creation of feedback items
def admin(request):
    return HttpResponse("Submit Feedback-item")

#Allows viewing of analytics
def analytics(request):
    return HttpResponse("See analytics")

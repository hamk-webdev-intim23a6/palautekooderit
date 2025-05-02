from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Feedback(models.Model):
    # Keys
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #Data
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5, validators=[
        MinValueValidator(1), MaxValueValidator(5)])
    positive = models.TextField(max_length=2500, blank=True)
    negative = models.TextField(max_length=2500, blank=True)
    ideas = models.TextField(max_length=2500, blank=True)
    anonymous = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.topic} - {self.rating}"
from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Feedback(models.Model):
    # Keys
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    #Data
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5, validators=[
        MinValueValidator(1), MaxValueValidator(5)])
    positive = models.TextField(max_length=2500, blank=True)
    negative = models.TextField(max_length=2500, blank=True)
    ideas = models.TextField(max_length=2500, blank=True)

    def __str__(self):
        return f"{self.topic} - {self.user} - {self.rating}"
        
    def save(self, *args, **kwargs):
        if self.user is not None:
            try:
                existing = Feedback.objects.get(user=self.user, topic=self.topic)
                if existing:
                    # Overwrite existing instead of creating a new one
                    self.pk = existing.pk

                    self.datetime = timezone.now()  # manually update timestamp
            except Feedback.DoesNotExist:
                pass  # No existing feedback, proceed as usual

        super().save(*args, **kwargs)
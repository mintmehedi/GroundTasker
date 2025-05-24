# tasks/models.py
from django.db import models
from django.conf import settings

class Task(models.Model):
    FLEX_CHOICES = [
        ('on_date', 'On date'),
        ('before_date', 'Before date'),
        ('flexible', "I'm flexible"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    due_type = models.CharField(max_length=20, choices=FLEX_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True, default="")
    bookmarked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bookmarked_tasks", blank=True)

    def __str__(self):
        return self.title

class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    task = models.ForeignKey(Task, related_name="offers", on_delete=models.CASCADE)
    offered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offered_by} offered {self.amount} for {self.task}"
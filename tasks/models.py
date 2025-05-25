from django.db import models
from django.conf import settings
from decimal import Decimal, InvalidOperation
from django.contrib.auth.models import User

class Task(models.Model):
    FLEX_CHOICES = [
        ('on_date', 'On date'),
        ('before_date', 'Before date'),
        ('flexible', "I'm flexible"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  
    due_type = models.CharField(max_length=20, choices=FLEX_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True, default="")
    bookmarked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bookmarked_tasks", blank=True)

    def __str__(self):
        try:
            return f"{self.title} (${self.budget or '0.00'})"
        except (InvalidOperation, TypeError):
            return self.title


class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    task = models.ForeignKey(Task, related_name="offers", on_delete=models.CASCADE)
    offered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return f"{self.offered_by.username} offered ${self.amount or '0.00'} for {self.task.title}"
        except (InvalidOperation, AttributeError, TypeError):
            return f"Offer for {self.task.title}"

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewee")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task")

    rating = models.CharField(max_length=15, null=True, blank=True)
    feedback = models.TextField(max_length=2000, null=True, blank=True)
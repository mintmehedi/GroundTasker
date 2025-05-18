from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10)

    ROLE_CHOICES = [
        ('get', 'Get things done'),
        ('earn', 'Earn money'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    ACCOUNT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business User'),
    ]
    account_type = models.CharField(max_length=12, choices=ACCOUNT_TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

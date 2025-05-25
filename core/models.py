from django.db import models
from django.contrib.auth.models import User
from tasks.models import *
from adminpanel.models import *
from django.urls import reverse
from django.utils.timezone import now

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    #message_id = models.PositiveIntegerField(null=True, blank=True)
    tag = models.CharField(max_length=15)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=now)

    def get_absolute_url(self):
        if self.tag == 'tasks' and self.task:
            return reverse('job_detail', kwargs={'task_id': self.task.id})
        elif self.tag == 'support' and self.ticket:
            return reverse('support_ticket_detail', kwargs={'ticket_id': self.ticket.id})
        else:
            return '#'
        
class MessageThread(models.Model):
    users = models.ManyToManyField(User)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=2000)\
    
class PremiumUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
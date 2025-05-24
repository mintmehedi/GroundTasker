from django.contrib import admin
from .models import Task, Offer  # Make sure Offer is imported

admin.site.register(Task)
admin.site.register(Offer)  # 👈 This is the missing line

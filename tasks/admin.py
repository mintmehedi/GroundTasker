from django.contrib import admin
from .models import Task, Offer, Review

admin.site.register(Task)
admin.site.register(Offer)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewee', 'task', 'rating')
    search_fields = ('reviewer__username', 'reviewee__username', 'task__title')
    raw_id_fields = ('reviewer', 'reviewee', 'task')
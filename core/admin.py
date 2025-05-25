from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'tag', 'task', 'ticket', 'short_message')
    list_filter = ('tag', 'recipient')
    search_fields = ('message', 'recipient__username', 'task__title', 'ticket__id')

    def short_message(self, obj):
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0  # No extra empty forms
    readonly_fields = ('sender', 'contents')
    can_delete = True

@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'created_at')
    filter_horizontal = ('users',)  # nicer widget for ManyToManyField
    inlines = [MessageInline]
    ordering = ('-created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'sender', 'short_contents')
    list_filter = ('sender', 'thread')
    search_fields = ('contents',)

    def short_contents(self, obj):
        return (obj.contents[:75] + '...') if len(obj.contents) > 75 else obj.contents
    short_contents.short_description = 'Message Preview'


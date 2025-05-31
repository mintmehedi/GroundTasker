# core/views.py
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from adminpanel.models import Ticket, TicketReply
from tasks.views import Offer
from .models import *
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        thread_id = self.kwargs.get("thread_id")  

        # Threads where user is poster or accepted offerer
        posted_tasks = Task.objects.filter(posted_by=user)
        accepted_tasks = Task.objects.filter(offers__offered_by=user, offers__status='accepted')

        threads = MessageThread.objects.filter(
            Q(task__in=posted_tasks) | Q(task__in=accepted_tasks),
            users=user
        ).distinct()

        context['threads'] = threads

        if thread_id:
            selected_thread = get_object_or_404(MessageThread, id=thread_id, users=user)
            context['selected_thread'] = selected_thread
            context["messages"] = selected_thread.message_set.select_related("sender").order_by("id")
        else:
            context['selected_thread'] = None
            context['messages'] = []

        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        thread_id = self.kwargs.get("thread_id")

        if not thread_id:
            # No thread specified; maybe redirect back or raise error
            return redirect('messages')  # or wherever your default is

        selected_thread = get_object_or_404(MessageThread, id=thread_id, users=user)
        contents = request.POST.get('contents', '').strip()

        if contents:
            Message.objects.create(thread=selected_thread, sender=user, contents=contents)

        # Redirect to the same thread page to avoid repost on refresh
        return redirect('messages_with_thread', thread_id=thread_id)
    

class NotificationsView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications.html'  # Your notifications template path
    context_object_name = 'notifications'  # Access in template as 'notifications'

    def get_queryset(self):
        user = self.request.user
        tag_filter = self.request.GET.get('tag', 'all').lower()

        qs = Notification.objects.filter(recipient=user).order_by('-created_at')

        if tag_filter != 'all':
            qs = qs.filter(tag=tag_filter)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current filter to template so you can highlight/filter UI buttons if needed
        context['current_filter'] = self.request.GET.get('tag', 'all').lower()
        return context

class SupportView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'support.html')

    def post(self, request):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        category = request.POST.get('category')
        message = request.POST.get('issue')
        file = request.FILES.get('attachment')

        Ticket.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            category=category,
            message=message,
            attachment=file
        )
        return redirect('support')

# keep this is a function do not make it class based
# it's for the real time messaging
@login_required
@require_GET
def message_api(request, thread_id):
    user = request.user
    try:
        thread = MessageThread.objects.get(id=thread_id, users=user)
    except MessageThread.DoesNotExist:
        return JsonResponse({'error': 'Thread not found'}, status=404)

    messages = thread.message_set.select_related('sender').order_by('id')
    return JsonResponse({
        'messages': [
            {
                'sender': msg.sender.username,
                'contents': msg.contents
            } for msg in messages
        ]
    })

from .models import PremiumUser
class SubscriptionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'subscription.html')

    def post(self, request, *args, **kwargs):
        PremiumUser.objects.create(user=request.user)
        return redirect('dashboard')
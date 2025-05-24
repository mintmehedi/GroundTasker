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
class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'messages.html'

    def get_context_data(self, **kwargs):
        selected_task_id = self.request.GET.get('task_id')
        sidebar_conversations = []

        # ✅ Dynamically fetch accepted offers by the logged-in user
        offers = Offer.objects.filter(offered_by=self.request.user, status='accepted').select_related('task')

        for offer in offers:
            task = offer.task
            sidebar_conversations.append({
                'task_id': task.id,
                'title': task.title,
                'username': task.posted_by.username,
                'active': str(task.id) == str(selected_task_id)
            })

        return {
            'conversations': sidebar_conversations,
            'selected_task_id': selected_task_id
        }

class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications.html'

    def get_context_data(self, **kwargs):
        user_tickets = Ticket.objects.filter(user=self.request.user)
        support_replies = TicketReply.objects.filter(ticket__in=user_tickets).order_by('-created_at')

        return {
            'support_replies': support_replies
        }

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

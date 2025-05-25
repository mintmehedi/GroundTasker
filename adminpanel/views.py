import os
from django.http import FileResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .models import Ticket, TicketReply
from core.models import Notification


@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'admin_dashboard.html'


@method_decorator(staff_member_required, name='dispatch')
class AdminTicketsListView(View):
    def get(self, request):
        status_filter = request.GET.get("status")
        tickets = Ticket.objects.all().order_by('-created_at')

        if status_filter in ["open", "closed"]:
            tickets = tickets.filter(status=status_filter)

        return render(request, 'admin_tickets.html', {
            'tickets': tickets,
            'current_status': status_filter
        })


@method_decorator(staff_member_required, name='dispatch')
class AdminTicketDetailView(View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        replies = TicketReply.objects.filter(ticket=ticket).order_by('created_at')
        return render(request, 'admin_ticket_detail.html', {
            'ticket': ticket,
            'replies': replies
        })

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if request.POST.get("action") == "close" and ticket.status == "open":
            ticket.status = "closed"
            ticket.save()
            return redirect('admin_ticket_detail', ticket_id=ticket.id)

        if request.POST.get("action") == "reply":
            message = request.POST.get("message", "")
            attachment = request.FILES.get("attachment")
            if message:
                recipient = ticket.user
                TicketReply.objects.create(
                    ticket=ticket,
                    message=message,
                    attachment=attachment
                )
                Notification.objects.create(
                    recipient=recipient,
                    ticket=ticket,
                    tag='support',
                    message=message
                )

        replies = TicketReply.objects.filter(ticket=ticket).order_by('created_at')
        return render(request, 'admin_ticket_detail.html', {
            'ticket': ticket,
            'replies': replies
        })


@method_decorator(staff_member_required, name='dispatch')
class AdminReportsView(TemplateView):
    template_name = 'admin_reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_users': 120,
            'total_tasks': 85,
            'tickets_open': 4,
            'tickets_closed': 9,
            'total_revenue': 13400.00
        }
        return context

# KEEP AS FUNCTION-BASED
# yes sir -kw
def download_attachment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not ticket.attachment:
        raise Http404("No attachment found.")

    file_path = ticket.attachment.path

    if not os.path.exists(file_path):
        raise Http404("File does not exist on disk.")

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
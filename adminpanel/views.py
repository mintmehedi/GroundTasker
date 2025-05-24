from django.http import FileResponse, Http404
import os
from django.conf import settings
from adminpanel.models import Ticket
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Ticket
from django.db.models import Q
from .models import Ticket, TicketReply
from django.core.files.uploadedfile import UploadedFile

@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@staff_member_required
def admin_tickets_list(request):
    status_filter = request.GET.get("status")
    tickets = Ticket.objects.all().order_by('-created_at')

    if status_filter in ["open", "closed"]:
        tickets = tickets.filter(status=status_filter)

    return render(request, 'admin_tickets.html', {
        'tickets': tickets,
        'current_status': status_filter
    })


@staff_member_required
def admin_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        if request.POST.get("action") == "close" and ticket.status == "open":
            ticket.status = "closed"
            ticket.save()
            return redirect('admin_ticket_detail', ticket_id=ticket.id)

    return render(request, 'admin_ticket_detail.html', {'ticket': ticket})


@staff_member_required
def admin_reports(request):
    stats = {
        'total_users': 120,
        'total_tasks': 85,
        'tickets_open': 4,
        'tickets_closed': 9,
        'total_revenue': 13400.00
    }
    return render(request, 'admin_reports.html', {'stats': stats})


def download_attachment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not ticket.attachment:
        raise Http404("No attachment found.")

    file_path = ticket.attachment.path

    if not os.path.exists(file_path):
        raise Http404("File does not exist on disk.")

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))



@staff_member_required
def admin_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        if request.POST.get("action") == "close" and ticket.status == "open":
            ticket.status = "closed"
            ticket.save()
            return redirect('admin_ticket_detail', ticket_id=ticket.id)

        # ✅ Admin reply handling
        if request.POST.get("action") == "reply":
            message = request.POST.get("message", "")
            attachment = request.FILES.get("attachment")
            if message:
                TicketReply.objects.create(
                    ticket=ticket,
                    message=message,
                    attachment=attachment
                )

    return render(request, 'admin_ticket_detail.html', {
        'ticket': ticket,
        'replies': TicketReply.objects.filter(ticket=ticket).order_by('created_at')
    })
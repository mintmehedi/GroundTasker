from django.urls import path
from .views import admin_dashboard, admin_tickets_list, admin_ticket_detail, admin_reports, download_attachment

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('tickets/', admin_tickets_list, name='admin_tickets'),
    path('tickets/<int:ticket_id>/', admin_ticket_detail, name='admin_ticket_detail'),
    path('reports/', admin_reports, name='admin_reports'),
    path('ticket/<int:ticket_id>/download/', download_attachment, name='download_attachment'),
]

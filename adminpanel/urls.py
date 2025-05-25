from django.urls import path
from .views import (
    AdminDashboardView,
    AdminTicketsListView,
    AdminTicketDetailView,
    AdminReportsView,
    download_attachment,  # still function-based
)
urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('tickets/', AdminTicketsListView.as_view(), name='admin_tickets'),
    path('tickets/<int:ticket_id>/', AdminTicketDetailView.as_view(), name='admin_ticket_detail'),
    path('reports/', AdminReportsView.as_view(), name='admin_reports'),
    path('ticket/<int:ticket_id>/download/', download_attachment, name='download_attachment'),
]

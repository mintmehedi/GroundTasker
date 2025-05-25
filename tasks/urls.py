from django.urls import path
from .views import (
    PostTaskView, JobListView, JobDetailView,
    ManageTasksView, MakeOfferView, ToggleBookmarkView,
    EditTaskView, DeleteTaskView, CompleteOfferView,
    WithdrawOfferView, AcceptOfferView, RejectOfferView
)

urlpatterns = [
    path('post/', PostTaskView.as_view(), name='post_task'),
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/<int:task_id>/', JobDetailView.as_view(), name='job_detail'),
    path('manage/', ManageTasksView.as_view(), name='manage_tasks'),
    path('offer/<int:task_id>/', MakeOfferView.as_view(), name='make_offer'),
    path('offer/withdraw/<int:offer_id>/', WithdrawOfferView.as_view(), name='withdraw_offer'),
    path('offer/complete/<int:offer_id>/', CompleteOfferView.as_view(), name='complete_offer'),
    path('offer/accept/<int:offer_id>/', AcceptOfferView.as_view(), name='accept_offer'),
    path('offer/reject/<int:offer_id>/', RejectOfferView.as_view(), name='reject_offer'),
    path('jobs/bookmark/<int:task_id>/', ToggleBookmarkView.as_view(), name='toggle_bookmark'),
    path('task/edit/<int:task_id>/', EditTaskView.as_view(), name='edit_task'),
    path('task/delete/<int:task_id>/', DeleteTaskView.as_view(), name='delete_task'),
]

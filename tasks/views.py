# tasks/views.py (updated for edit/withdraw offer support)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Task, Offer

class PostTaskView(LoginRequiredMixin, View):
    def get(self, request):
        task_id = request.GET.get('edit')
        task = None
        if task_id:
            task = get_object_or_404(Task, id=task_id, posted_by=request.user)

        categories = [
            "Cleaning", "Gardening", "Repairs", "Car Detailing", "Moving",
            "Delivery", "Pet Care", "Personal Assistant", "Handyman"
        ]
        return render(request, 'post_task.html', {
            'categories': categories,
            'task': task
        })

    def post(self, request):
        task_id = request.GET.get('edit')
        if task_id:
            task = get_object_or_404(Task, id=task_id, posted_by=request.user)
            task.title = request.POST.get("title")
            task.description = request.POST.get("description")
            task.location = request.POST.get("location")
            task.category = request.POST.get("category")
            task.budget = request.POST.get("budget")
            task.due_date = request.POST.get("due_date")
            task.due_type = request.POST.get("due_type")
            task.save()
        else:
            Task.objects.create(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                location=request.POST.get("location"),
                category=request.POST.get("category"),
                budget=request.POST.get("budget"),
                due_date=request.POST.get("due_date"),
                due_type=request.POST.get("due_type"),
                posted_by=request.user
            )
        return redirect('job_list')

class JobListView(View):
    def get(self, request):
        title = request.GET.get('title', '')
        location = request.GET.get('location', '')
        category = request.GET.get('category', '')

        filters = {}
        if title:
            filters['title__icontains'] = title
        if location:
            filters['location__icontains'] = location
        if category:
            filters['category__icontains'] = category

        tasks = Task.objects.filter(**filters)
        locations = Task.objects.values_list('location', flat=True).distinct()
        categories = [
            "Cleaning", "Gardening", "Repairs", "Car Detailing", "Moving",
            "Delivery", "Pet Care", "Personal Assistant", "Handyman"
        ]

        return render(request, 'job_list.html', {
            'tasks': tasks,
            'locations': locations,
            'categories': categories,
        })

class JobDetailView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'job_detail.html', {'task': task})

class MakeOfferView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        offer_id = request.GET.get('edit_offer')
        offer = None

        if offer_id:
            offer = get_object_or_404(Offer, id=offer_id, offered_by=request.user, task=task)

        return render(request, 'make_offer.html', {
            'task': task,
            'offer': offer  # used to pre-fill the form if editing
        })

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        offer_id = request.GET.get('edit_offer')
        amount = request.POST.get('amount')
        message = request.POST.get('message')
        availability = request.POST.get('availability')
        file = request.FILES.get('attachment')

        if offer_id:
            # Editing existing offer
            offer = get_object_or_404(Offer, id=offer_id, offered_by=request.user, task=task)
            offer.amount = amount
            offer.message = message
            offer.save()
        else:
            # Creating new offer
            Offer.objects.create(
                task=task,
                offered_by=request.user,
                amount=amount,
                message=message,
                status='pending'
            )

        return redirect('manage_tasks')

class ManageTasksView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            'posted_tasks': Task.objects.filter(posted_by=user),
            'applied_offers': Offer.objects.filter(offered_by=user, status='pending'),
            'engaged_offers': Offer.objects.filter(offered_by=user, status='accepted'),
            'bookmarked_tasks': user.bookmarked_tasks.all(),
            'completed_tasks': Offer.objects.filter(offered_by=user, status='completed'),
            'incoming_offers': Offer.objects.filter(task__posted_by=user).exclude(status='completed')
        }
        return render(request, 'manage_tasks.html', context)


@method_decorator([login_required, require_POST], name='dispatch')
class ToggleBookmarkView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if request.user in task.bookmarked_by.all():
            task.bookmarked_by.remove(request.user)
            return JsonResponse({'status': 'removed'})
        else:
            task.bookmarked_by.add(request.user)
            return JsonResponse({'status': 'added'})

class EditTaskView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, posted_by=request.user)
        categories = [
            "Cleaning", "Gardening", "Repairs", "Car Detailing", "Moving",
            "Delivery", "Pet Care", "Personal Assistant", "Handyman"
        ]
        return render(request, 'post_task.html', {
            'task': task,
            'categories': categories
        })

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, posted_by=request.user)
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.location = request.POST.get("location")
        task.category = request.POST.get("category")
        task.budget = request.POST.get("budget")
        task.due_date = request.POST.get("due_date")
        task.due_type = request.POST.get("due_type")
        task.save()
        return redirect('manage_tasks')

class DeleteTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, posted_by=request.user)
        task.delete()
        return redirect('manage_tasks')

class CompleteOfferView(LoginRequiredMixin, View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id, offered_by=request.user)
        offer.status = 'completed'
        offer.save()
        return redirect('manage_tasks')

class WithdrawOfferView(LoginRequiredMixin, View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id, offered_by=request.user)
        offer.delete()
        return redirect('manage_tasks')



@method_decorator(login_required, name='dispatch')
class AcceptOfferView(View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        if offer.task.posted_by == request.user:
            offer.status = 'accepted'
            offer.save()
        return redirect('manage_tasks')

@method_decorator(login_required, name='dispatch')
class RejectOfferView(View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        if offer.task.posted_by == request.user:
            offer.status = 'rejected'
            offer.save()
        return redirect('manage_tasks')
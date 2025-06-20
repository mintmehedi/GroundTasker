from django.db.models import Q
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
from decimal import Decimal, InvalidOperation
from .models import Task, Offer, Review
from django.db.models import Avg
from accounts.models import *
from core.models import Notification
from core.models import MessageThread

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
        try:
            budget = Decimal(request.POST.get("budget") or '0.00')
        except InvalidOperation:
            budget = Decimal('0.00')

        if task_id:
            task = get_object_or_404(Task, id=task_id, posted_by=request.user)
            task.title = request.POST.get("title")
            task.description = request.POST.get("description")
            task.location = request.POST.get("location")
            task.category = request.POST.get("category")
            task.budget = budget
            task.due_date = request.POST.get("due_date")
            task.due_type = request.POST.get("due_type")
            task.save()
        else:
            Task.objects.create(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                location=request.POST.get("location"),
                category=request.POST.get("category"),
                budget=budget,
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

        from django.db.models import Count, Q
        tasks = Task.objects.filter(**filters).annotate(
            accepted_or_completed=Count('offers', filter=Q(offers__status__in=['accepted', 'completed']))
        ).filter(accepted_or_completed=0)

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

        if Offer.objects.filter(task=task, status='accepted').exists():
            return redirect('job_list')

        offer_id = request.GET.get('edit_offer')
        offer = None

        if offer_id:
            offer = get_object_or_404(Offer, id=offer_id, offered_by=request.user, task=task)

        return render(request, 'make_offer.html', {
            'task': task,
            'offer': offer
        })

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if Offer.objects.filter(task=task, status='accepted').exists():
            return redirect('job_list')

        offer_id = request.GET.get('edit_offer')
        try:
            amount = Decimal(request.POST.get('amount') or '0.00')
        except InvalidOperation:
            amount = Decimal('0.00')

        message = request.POST.get('message')
        availability = request.POST.get('availability')
        file = request.FILES.get('attachment')

        if offer_id:
            offer = get_object_or_404(Offer, id=offer_id, offered_by=request.user, task=task)
            offer.amount = amount
            offer.message = message
            offer.save()
        else:
            offer = Offer.objects.create(
                task=task,
                offered_by=request.user,
                amount=amount,
                message=message,
                status='pending'
            )
            Notification.objects.create(recipient=offer.task.posted_by ,task=offer.task,tag='tasks', message=f"A new offer has been made on your task for ${amount}.")

        return redirect('manage_tasks')

class ManageTasksView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posted_tasks = Task.objects.filter(posted_by=user).prefetch_related('offers')

        # Map task.id → accepted offer object
        accepted_offers = {
            task.id: next((o for o in task.offers.all() if o.status == 'accepted'), None)
            for task in posted_tasks
        }

        # Map task.id → boolean if there's any completed offer
        has_completed_offers = {
            task.id: task.offers.filter(status='completed').exists()
            for task in posted_tasks
        }

        context = {
            'posted_tasks': posted_tasks,
            'accepted_offers': accepted_offers,
            'has_completed_offers': has_completed_offers,  # <-- added for template fix
            'applied_offers': Offer.objects.filter(offered_by=user, status='pending'),
            'engaged_offers': Offer.objects.filter(
                Q(offered_by=user) | Q(task__posted_by=user),
                status='accepted'
            ),
            'bookmarked_tasks': user.bookmarked_tasks.all(),
            'completed_tasks': Offer.objects.filter(
                Q(offered_by=user) | Q(task__posted_by=user),
                status='completed'
            ),
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
        offer = get_object_or_404(Offer, id=offer_id)

        if offer.offered_by == request.user or offer.task.posted_by == request.user:
            offer.status = 'completed'
            offer.save()
            Notification.objects.create(recipient=offer.task.posted_by ,task=offer.task,tag='tasks', message=f"Task '{offer.task} has been set as completed.")

        

        return redirect('manage_tasks')

class WithdrawOfferView(LoginRequiredMixin, View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id, offered_by=request.user)
        Notification.objects.create(recipient=offer.task.posted_by,task=offer.task,tag='tasks',message=f"{request.user} has withdrawn their offer on post '{offer.task.title}'.")
        offer.delete()
        return redirect('manage_tasks')
        
@method_decorator(login_required, name='dispatch')
class AcceptOfferView(View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)

        if offer.task.posted_by == request.user:
            offer.status = 'accepted'
            offer.save()

            thread, created = MessageThread.objects.get_or_create(task=offer.task)
            thread.users.add(offer.task.posted_by, offer.offered_by)

            Notification.objects.create(
                recipient=offer.offered_by,
                task=offer.task,
                tag='offers',
                message=f"{offer.task.posted_by} has accepted your offer on task '{offer.task.title}'."
            )

            Offer.objects.filter(task=offer.task).exclude(id=offer.id).update(status='rejected')

        return redirect('manage_tasks')


@method_decorator(login_required, name='dispatch')
class RejectOfferView(View):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)

        if offer.task.posted_by == request.user:
            if offer.status == 'accepted':
                try:
                    thread = MessageThread.objects.get(task=offer.task)
                    thread.delete()
                except MessageThread.DoesNotExist:
                    pass

            offer.status = 'rejected'
            offer.save()

            Notification.objects.create(
                recipient=offer.offered_by,
                task=offer.task,
                tag='offers',
                message=f"{offer.task.posted_by} has declined your offer on task '{offer.task.title}'."
            )

        return redirect('manage_tasks')
    
class CreateReview(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        rating = request.POST.get('rating')
        feedback = request.POST.get('comment')
        task = get_object_or_404(Task, id=task_id)
        reviewee = task.posted_by
        revieweeProfile = get_object_or_404(Profile, user=task.posted_by)

        review = Review.objects.create(reviewer=request.user,reviewee=task.posted_by,task=task,rating=rating,feedback=feedback)

        reviews_qs = Review.objects.filter(reviewee=reviewee).select_related('reviewer')
        revieweeProfile.average_rating = round(reviews_qs.aggregate(avg=Avg('rating'))['avg'] or 0, 2)
        revieweeProfile.save()
        Notification.objects.create(recipient=reviewee,task=task,tag='tasks',message=f"{request.user} has rated you {review.rating} stars.")

        return redirect('manage_tasks')
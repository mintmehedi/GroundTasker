from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse_lazy
import requests
import json

from .forms import ProfileForm
from .models import Profile
from tasks.models import Task

# -------------------- Main Views -------------------- #

class HomePageView(TemplateView):
    template_name = "home.html"

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('setup_profile')

class CustomLoginView(LoginView):
    template_name = 'login.html'

class LogoutConfirmView(TemplateView):
    template_name = 'logout_confirm.html'

@csrf_exempt
def auspost_proxy(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"error": "Missing search term"}, status=400)

    try:
        response = requests.get(
            "https://digitalapi.auspost.com.au/postcode/search.json",
            params={"q": query},
            headers={"auth-key": "7eb48f5c-1d0b-4458-b8b2-ed140923b2e7"}
        )
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# -------------------- Profile Setup -------------------- #

class ProfileSetupView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'profile_setup.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
        return render(request, 'profile_setup.html', {'form': form})

# -------------------- Edit Profile -------------------- #

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        certification_options = [
            'Police Check', 'Trade License', 'Working With Children',
            'First Aid', 'Insurance', 'Other'
        ]
        return render(request, 'edit_profile.html', {
            'user': request.user,
            'profile': profile,
            'certification_options': certification_options,
        })

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile.bio = request.POST.get('bio')

        raw_skills = request.POST.get('skills')
        try:
            parsed = json.loads(raw_skills)
            profile.skills = ', '.join([item["value"].strip() for item in parsed])
        except:
            profile.skills = raw_skills

        profile.postcode = request.POST.get('location')

        raw_certs = request.POST.get('certifications')
        try:
            parsed_certs = json.loads(raw_certs)
            profile.certifications = ', '.join([item["value"].strip() for item in parsed_certs])
        except:
            profile.certifications = raw_certs

        profile.save()
        return redirect('public_profile', username=user.username)

# -------------------- Public Profile -------------------- #

class PublicProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile, _ = Profile.objects.get_or_create(user=user)
        skills = [s.strip() for s in profile.skills.split(',')] if profile.skills else []
        cert_list = [c.strip() for c in profile.certifications.split(',')] if profile.certifications else []
        posted_tasks = Task.objects.filter(posted_by=user)

        return render(request, 'public_profile.html', {
            'user_profile': user,
            'profile': profile,
            'skills': skills,
            'cert_list': cert_list,
            'posted_tasks': posted_tasks
        })

# -------------------- Change Email & Password -------------------- #

class ChangeEmailView(LoginRequiredMixin, TemplateView):
    template_name = 'change_email.html'

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'change_password.html'

# -------------------- Dashboard -------------------- #

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'completed_jobs': 25,
            'avg_rating': 4.8,
            'total_feedback': 35,
            'total_earnings': 24450.00,
        }
        context['completed_jobs'] = [
            {'title': 'Cleaning Kitchen', 'date': 'May 10, 2025', 'client': 'Jane Smith', 'amount': '$120.00', 'rating': 4.9},
            {'title': 'Weeding my garden', 'date': 'May 15, 2025', 'client': 'Mark Liu', 'amount': '$250.00', 'rating': 4.8},
        ]
        context['reviews'] = [
            {'client': 'Mark Liu', 'rating': 4.8, 'comment': 'I’m very satisfied with the work......'},
            {'client': 'Jane Smith', 'rating': 4.9, 'comment': 'I’m very satisfied with the work......'},
        ]
        return context

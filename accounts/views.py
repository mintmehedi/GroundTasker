from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

from .forms import ProfileForm
from .models import Profile


# -------------------- Main Views -------------------- #

# Homepage View
class HomePageView(TemplateView):
    template_name = "home.html"

# Register View with auto-login + redirect to profile setup
class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('setup_profile')


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Logout confirmation view
class LogoutConfirmView(TemplateView):
    template_name = 'logout_confirm.html'

# Profile Setup View
@login_required
def profile_setup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')  
    else:
        form = ProfileForm()
    return render(request, 'profile_setup.html', {'form': form})


# -------------------- Australia Post API Proxy -------------------- #

@csrf_exempt
def auspost_proxy(request):
    """
    Proxy to call Australia Post API from server-side (avoids CORS).
    """
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



# -------------------- View Profile -------------------- #
@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        profile.skills = request.POST.get('skills')
        profile.location = request.POST.get('location')
        profile.save()
    
    return render(request, 'view_profile.html', {'user': request.user, 'profile': profile})

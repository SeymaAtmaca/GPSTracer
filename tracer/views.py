from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DetailView, CreateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import User


class UserLoginView(LoginView):
    template_name = 'tracer/login.html'

@login_required
def user_profile(request):
    profile, created = User.objects.get_or_create(user=request.user)
    return render(request, 'tracer/profile.html', {'profile': profile})

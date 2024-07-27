from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, UpdateView, DetailView, CreateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm


class UserLoginView(LoginView):
    template_name = 'tracer/login.html'

    def form_valid(self, form):
        # Kullanıcı giriş yaptıktan sonra yönlendirme
        if self.request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/profile/')

class HomeView(LoginView):
    template_name = 'tracer/home.html'
    context_object_name = 'home'


@login_required
def user_profile(request):
    return render(request, 'tracer/profile.html', {'profile': request.user})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    
    # Formu template'e göndermek
    return render(request, 'tracer/signup.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import ListView, UpdateView, DetailView, CreateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm


class UserLoginView(LoginView):
    template_name = 'tracer/login.html'

    def form_valid(self, form):
        # Kullanıcı giriş yaptıktan sonra yönlendirme
        if self.request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/profile/')
        
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'tracer/edit_profile.html', {'form': form})


class HomeView(LoginView):
    template_name = 'tracer/home.html'
    context_object_name = 'home'


@login_required
def user_profile(request):
    friends = User.objects.exclude(id=request.user.id)  
    return render(request, 'tracer/profile.html', {'profile': request.user, 'friends': friends})



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
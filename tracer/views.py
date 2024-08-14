from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import ListView, UpdateView, DetailView, CreateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserSearchForm
from django.http import JsonResponse
from django.db.models import Q


User = get_user_model()

@login_required
def send_friend_request(request, user_id):
    user_to_request = User.objects.get(id=user_id)
    if user_to_request:
        # Burada arkadaşlık isteği oluşturma işlemini gerçekleştirebilirsiniz.
        # Örneğin, bir FriendRequest modeli varsa, bu modeli kullanarak istek oluşturabilirsiniz.
        pass
    return redirect('profile')

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
    search_form = UserSearchForm()
    search_results = []

    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        if query:
            search_results = User.objects.filter(
                Q(username__icontains=query) | Q(email__icontains=query),
                is_superuser=False
            ).exclude(id=request.user.id)
            
            results = []
            for user in search_results:
                results.append({
                    'id': user.id,
                    'username': user.username,
                    'profile_picture': user.profile_picture.url if user.profile_picture else 'https://via.placeholder.com/40',
                })
            return JsonResponse({'results': results})

    friends = User.objects.exclude(id=request.user.id)

    context = {
        'profile': request.user,
        'friends': friends,
        'search_form': search_form,
        'search_results': search_results,
    }

    return render(request, 'tracer/profile.html', context)



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
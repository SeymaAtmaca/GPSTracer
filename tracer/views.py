from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import User, Friendship
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserSearchForm
from django.http import JsonResponse
from django.db.models import Q, Prefetch
from .models import FriendRequest, Notification, Location, Lists, ListItems
from datetime import datetime
from .forms import ListCreateForm, ListItemForm
import json
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@login_required
def send_friend_request(request):
    if request.method == 'POST':
        active_user_id = request.POST.get('active_user_id')
        target_user_id = request.POST.get('target_user_id')

        sender = User.objects.get(id=active_user_id)
        receiver = User.objects.get(id=target_user_id)

        # Friend request oluştur
        friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)

        # Bildirim gönder
        Notification.objects.create(
            recipient=receiver,
            message=f"{sender.username} sent you a friend request.",
            link=f"/user/{sender.id}/"
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_user_friends(user):
    friendships = Friendship.objects.filter(
        Q(sender=user, status='accepted') | Q(receiver=user, status='accepted')
    )
    friends = []
    for friendship in friendships:
        # Arkadaşlık ilişkisini oluşturan diğer kullanıcıyı bul
        friend = friendship.receiver if friendship.sender == user else friendship.sender
        friends.append(friend)
    return friends



class UserLoginView(LoginView):
    template_name = 'tracer/login.html'
    def form_valid(self, form):
        user = form.get_user() 
        login(self.request, user) 

        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        if user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('profile')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.show_locations = 'show_profile' in request.POST
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'tracer/edit_profile.html', {'form': form})

@login_required
def add_friend(request):
    if request.method == 'POST':
        active_user_id = request.POST.get('active_user_id')
        target_user_id = request.POST.get('target_user_id')

        if not active_user_id or not target_user_id:
            return JsonResponse({'status': 'error', 'message': 'Invalid user IDs'})

        sender = get_object_or_404(User, id=active_user_id)
        target = get_object_or_404(User, id=target_user_id)

        
        Friendship.objects.create(sender=sender, receiver=target, status="accepted")
        # if sender == target:
        #     return JsonResponse({'status': 'error', 'message': 'You cannot add yourself as a friend'})

        # sender.friends.add(target)
        # target.friends.add(sender) 
        return JsonResponse({'status': 'success', 'message': 'Friend added successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        

class HomeView(LoginView):
    template_name = 'tracer/home.html'
    context_object_name = 'home'


def show_profile(request, id):
    user = get_object_or_404(User, id=id)  # ID'ye göre kullanıcıyı al
    user_friends = get_user_friends(user)
    return render(request, 'tracer/profile.html', {'profile': user, 'user_friends': user_friends})

def visit_profile(request, id):
    # ID'ye göre kullanıcıyı al
    user = get_object_or_404(User, id=id)
    
    # Ziyaret eden kişi ve profil sahibi arkadaş mı?
    is_friend = Friendship.objects.filter(
        sender=user, receiver=request.user, status='accepted'
    ).exists() or Friendship.objects.filter(
        sender=request.user, receiver=user, status='accepted'
    ).exists()

    # Bildirim varsa okundu olarak işaretle
    if request.method == 'POST':
        notification_id = request.POST.get('notificationId')
        notification = Notification.objects.filter(id=notification_id).first()
        if notification:
            notification.is_read = True
            notification.save()
    user_friends = get_user_friends(user)

    # Şablona is_friend değişkenini de ekle
    context = {
        'profile': user,
        'user_friends' : user_friends,
        'is_friend': is_friend,
    }

    return render(request, 'tracer/user.html', context)

def mark_as_read(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        
        # Bildirimi bul ve okundu olarak işaretle
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def user_profile(request):
    search_form = UserSearchForm()
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        search_results = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query),
            is_superuser=False
        ).exclude(id=request.user.id)

        results = [
            {
                'id': user.id,
                'username': user.username,
                'profile_picture': user.profile_picture.url if user.profile_picture else 'https://via.placeholder.com/40',
            }
            for user in search_results
        ]
        return JsonResponse({'results': results})

    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    friends = get_user_friends(request.user)
    lists_with_items = Lists.objects.filter(user=request.user).prefetch_related(
        Prefetch('listitems_set', queryset=ListItems.objects.all())
    )

    # Prepare context data
    lists_data = []
    for list_obj in lists_with_items:
        items = list_obj.listitems_set.all()  # Get associated items
        list_data = {
            'id': list_obj.id,
            'name': list_obj.name,
            'items': [{'id': item.id, 'name': item.item_name, 'latitude': item.latitude, 'longitude': item.longitude} for item in items]
        }
        lists_data.append(list_data)

    context = {
        'profile': request.user,
        'friends': friends,
        'search_form': search_form,
        'notifications': notifications,
        'lists' : lists_data
        
    }

    return render(request, 'tracer/profile.html', context)


@login_required
def map(request):
    show_item_location = False

    if request.method == "POST" and request.POST.get('itemLat'):
        item_id = request.POST.get('itemId')
        item_location_lat = request.POST.get('itemLat')
        item_location_long = request.POST.get('itemLong')
        item_name = request.POST.get('itemName')
        show_item_location = True

    user = request.user
    friends = get_user_friends(request.user)
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    lists = Lists.objects.filter(user=user)

    friends_locations = []
    for friend in friends:
        last_location = Location.objects.filter(user=friend).order_by('-timestamp').first()
        if last_location:
            friends_locations.append({
                'id': str(friend.id),
                'username': friend.username,
                'profile_picture': friend.profile_picture.url if friend.profile_picture else None,
                'latitude': last_location.latitude,
                'longitude': last_location.longitude,
            })

    context = {
        'profile': user,
        'friends_locations': friends_locations,
        'notifications': notifications,
        'lists': lists,
        'show_item_location': show_item_location,
        'item_note' : ""
    }

    if show_item_location:
        print(item_id)
        item_note = ListItems.objects.filter(id = item_id).first();
        print(item_note)
        item_note = item_note.notes;
        print(item_note)
        context.update({
            'item_location_lat': item_location_lat,
            'item_location_long': item_location_long,
            'item_name': item_name,
            'show_item_location': show_item_location,
            'item_note' : str(item_note)
        })

    return render(request, 'tracer/map.html', context)
    


def create_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get("name")

        if not name:
            return JsonResponse({"error": "Name field is required."}, status=400)

        list_form = ListCreateForm({'name': name})  
        if list_form.is_valid():  
            # Yeni liste oluştur
            new_list = list_form.save(commit=False)
            new_list.user = request.user 
            new_list.save() 
            return JsonResponse({'success': True, 'list_id': new_list.id})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def create_list_item(request):
    if request.method == 'POST':
        try:
            # JSON verisini al
            data = json.loads(request.body)
            list_id = data.get("list_name")      # Liste ID'si
            item_name = data.get("item_name")    # Öğe adı
            item_note = data.get('item_note')
            latitude = data.get("latitude")       # Enlem
            longitude = data.get("longitude")     # Boylam

            # Gerekli alanların kontrolü
            if not all([list_id, item_name, latitude, longitude]):
                return JsonResponse({
                    'success': False,
                    'error': 'Tüm alanlar gereklidir.'
                }, status=400)

            # Liste nesnesini bul
            try:
                list_obj = Lists.objects.get(id=list_id, user=request.user)
            except Lists.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Liste bulunamadı.'
                }, status=404)

            # Yeni liste öğesi oluştur
            list_item = ListItems.objects.create(
                list_name=list_obj,
                item_name=item_name,
                latitude=latitude,
                longitude=longitude,
                notes = item_note
            )

            return JsonResponse({
                'success': True,
                'item_id': str(list_item.id)
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Geçersiz JSON verisi.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'İzin verilmeyen metod.'
    }, status=405)



def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('sessionid')
    return response


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'tracer/signup.html', {'form': form})
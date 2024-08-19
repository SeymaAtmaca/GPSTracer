from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
]

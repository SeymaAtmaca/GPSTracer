from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('add_friend/', views.send_friend_request, name='add_friend'),
    # path('profile/<uuid:id>/', views.show_profile, name='show_profile'),
    path('user/<uuid:id>/', views.visit_profile, name='visit_profile'),
    path('map/', views.map, name='map'),
    
]

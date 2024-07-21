from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    #path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),

]
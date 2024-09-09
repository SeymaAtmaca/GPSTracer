from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# User table model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='tracer_users',  # related_name ekledik
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='tracer_users',  # related_name ekledik
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Diğer gerekli alanlar

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    link = models.URLField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Diğer gerekli alanlar


    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"
    
# Location table model
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.latitude}, {self.longitude}'

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# User model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    show_friend_list = models.BooleanField(default=False)
    show_locations = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Friendship(models.Model):
    sender = models.ForeignKey(User, related_name='sent_friendships', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_friendships', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('accepted', 'Accepted')], default='sent')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')  # Prevents duplicate friend requests between the same users

    def __str__(self):
        return f"{self.sender} -> {self.receiver} | Status: {self.status}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friend request from {self.sender} to {self.receiver}"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    link = models.URLField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"


# Location model
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.latitude}, {self.longitude}'

class Lists(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ListItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    list_name = models.ForeignKey(Lists, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
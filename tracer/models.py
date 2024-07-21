from django.db import models
from django.contrib.auth.models import User

# User table model
class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=250)
    lastName = models.CharField(max_length=250)
    isActive = models.BooleanField(default=True)
    picture = models.ImageField(upload_to = 'profile_pics')

    def __str__(self):
        return self.user.username

# Location table model
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.latitude}, {self.longitude}'

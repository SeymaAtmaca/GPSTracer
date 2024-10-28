from django.contrib import admin

from .models import User, Notification, FriendRequest, Location, Friendship

# admin.site.register(User)
# admin.site.register(FriendRequest)
# admin.site.register(Location)
# admin.site.register(Notification)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','first_name','last_name','isActive')
    list_filter = ('isActive',)
    #filter_horizontal = ('friends',)
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'created_at', 'is_read',)
    list_filter = ('is_read', 'created_at',)

@admin.register(Friendship)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'timestamp',)
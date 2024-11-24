from django.contrib import admin

from .models import User, Notification, FriendRequest, Location, Friendship, Lists, ListItems, Images

# admin.site.register(User)
# admin.site.register(FriendRequest)
# admin.site.register(Location)
# admin.site.register(Notification)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','first_name','last_name','profile_picture', 'isActive')
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


@admin.register(Lists)
class ListsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','user')

@admin.register(ListItems)
class ListItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'list_name', 'item_name', 'notes', 'latitude', 'longitude')

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'list_item', 'image', 'uploaded_at')
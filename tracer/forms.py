from django.forms import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Lists, ListItems

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2')

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture')

class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search for users', max_length=100)

class ListCreateForm(forms.ModelForm):
    class Meta:
        model = Lists
        fields = ['name']

class ListItemForm(forms.ModelForm):
    class Meta:
        model = ListItems
        fields = ['item_name', 'latitude', 'longitude']
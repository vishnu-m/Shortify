

from django import forms

from django.contrib.auth.forms import  UserChangeForm
from django.contrib.auth.models import  User

from .models import UserPhoneNumber
class UserEditForm(UserChangeForm):

    class Meta:

        model = User
        fields = ('email' , 'first_name','last_name','password')

class ImageChangeForm(forms.Form):

    image = forms.ImageField(

        label= 'Browse',
    )







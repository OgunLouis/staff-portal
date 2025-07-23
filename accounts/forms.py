from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class StaffSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'phone_number',
            'password1',
            'password2',
            'address',
            'photo',
            'next_of_kin',
            'next_of_kin_contact',
            'next_of_kin_address'
        ]


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'address', 'next_of_kin', 'photo','next_of_kin_contact', 'full_name','phone_number','next_of_kin_address']

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

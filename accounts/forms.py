from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class StaffSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'password1',
            'password2',
            'address',
            'next_of_kin',
            'next_of_kin_contact',
            'photo',
        ]


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'address', 'next_of_kin', 'photo','next_of_kin_contact', 'full_name']

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

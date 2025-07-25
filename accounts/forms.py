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

from django import forms
from .models import Loan

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount', 'months_to_repay', 'reason']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '100000',
                'placeholder': 'Enter amount (min ₦100,000)'
            }),
            'months_to_repay': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter number of months'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'State your reason for requesting the loan'
            }),
        }
        labels = {
            'amount': 'Loan Amount (₦)',
            'months_to_repay': 'Repayment Duration (in months)',
            'reason': 'Reason for Loan',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 100000:
            raise forms.ValidationError("Minimum loan amount is ₦100,000.")
        return amount

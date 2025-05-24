# accounts/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'postcode', 'role', 'account_type']
        widgets = {
            'role': forms.RadioSelect(),
            'account_type': forms.RadioSelect()
        }

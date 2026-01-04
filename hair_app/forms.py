from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import HairDonor, HairRequest, ContactMessage, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class HairDonorForm(forms.ModelForm):
    class Meta:
        model = HairDonor
        exclude = ['user', 'status', 'donation_date', 'created_at', 'updated_at']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'hair_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length in inches', 'step': '0.1'}),
            'hair_type': forms.Select(attrs={'class': 'form-control'}),
            'hair_color': forms.Select(attrs={'class': 'form-control'}),
            'hair_condition': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe hair condition (dyed, chemically treated, etc.)'}),
            'willing_to_donate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HairRequestForm(forms.ModelForm):
    class Meta:
        model = HairRequest
        exclude = ['user', 'request_status', 'matched_donor', 'admin_notes', 'created_at', 'updated_at']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Patient age'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'patient_type': forms.Select(attrs={'class': 'form-control'}),
            'medical_condition': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe medical condition'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'required_hair_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum length in inches', 'step': '0.1'}),
            'preferred_hair_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred color (optional)'}),
            'preferred_hair_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred type (optional)'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital name'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doctor name'}),
            'doctor_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doctor contact'}),
            'medical_certificate': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone', 'bio', 'address', 'city', 'state', 'pincode', 'date_of_birth']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Full Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )
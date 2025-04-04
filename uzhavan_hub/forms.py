from django import forms
from django.contrib.auth.models import User
from .models import Farmer, Produce, UzhavanHub

class FarmerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['phone', 'village', 'district', 'state', 
                 'aadhaar_number', 'bank_account', 'ifsc_code']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['phone', 'village', 'district', 'bank_account', 'ifsc_code']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProduceForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = ['name', 'category', 'quantity', 'grade', 
                 'price_per_kg', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'price_per_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class HubSubmissionForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = ['hub']
        widgets = {
            'hub': forms.Select(attrs={'class': 'form-control'}),
        }

class HubCreationForm(forms.ModelForm):
    class Meta:
        model = UzhavanHub
        fields = ['name', 'location', 'manager', 'contact_number',
                 'latitude', 'longitude', 'operational_hours']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'operational_hours': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HubEditForm(forms.ModelForm):
    class Meta:
        model = UzhavanHub
        fields = ['name', 'location', 'contact_number',
                 'latitude', 'longitude', 'operational_hours']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'operational_hours': forms.TextInput(attrs={'class': 'form-control'}),
        }
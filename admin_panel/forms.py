from django import forms
from uzhavan_hub.models import UzhavanHub
from .models import Dispute

class HubForm(forms.ModelForm):
    class Meta:
        model = UzhavanHub
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'operational_hours': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DisputeResolutionForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ['resolution']
        widgets = {
            'resolution': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
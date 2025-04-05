from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .models import Farmer, Produce, UzhavanHub

STATE_CHOICES = [
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Kerala', 'Kerala'),
    ('Karnataka', 'Karnataka'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Telangana', 'Telangana'),
]

class FarmerRegistrationForm(forms.ModelForm):
    state = forms.ChoiceField(
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Farmer
        fields = ['phone', 'village', 'district', 'state',
                 'aadhaar_number', 'bank_account', 'ifsc_code']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{10,15}',
                'title': 'Enter 10-15 digit phone number'
            }),
            'village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your village name'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your district'
            }),
            'aadhaar_number': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{12}',
                'title': '12 digit Aadhaar number',
                'placeholder': 'Enter 12-digit Aadhaar'
            }),
            'bank_account': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{9,18}',
                'title': '9-18 digit account number',
                'placeholder': 'Enter bank account number'
            }),
            'ifsc_code': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[A-Z]{4}0[A-Z0-9]{6}',
                'title': '11 character IFSC code',
                'placeholder': 'Enter IFSC code'
            }),
        }
        help_texts = {
            'ifsc_code': 'Format: ABCD0123456',
            'aadhaar_number': '12 digits without spaces'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

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
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Always show all hubs (remove district filtering)
        self.fields['hub'].queryset = UzhavanHub.objects.all().order_by('name')
        
        # Make hub field required
        self.fields['hub'].required = True

    class Meta:
        model = Produce
        fields = ['name', 'category', 'quantity', 'grade', 
                 'price_per_kg', 'description', 'image', 'hub']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Organic Tomatoes'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.1',
                'step': '0.1'
            }),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'price_per_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'step': '0.5'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your produce...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'hub': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero")
        return quantity

class HubCreationForm(forms.ModelForm):
    class Meta:
        model = UzhavanHub
        fields = ['name', 'location', 'manager', 'contact_number',
                 'latitude', 'longitude', 'operational_hours']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Chennai Organic Hub'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full address with landmark'
            }),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{10,15}'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
            'operational_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 8 AM - 6 PM, Monday-Saturday'
            }),
        }
        help_texts = {
            'latitude': 'Get coordinates from Google Maps',
            'operational_hours': 'Specify working days and times'
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
class HubSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)
        
        if farmer:
            # Filter hubs near the farmer's location
            self.fields['hub'].queryset = UzhavanHub.objects.filter(
                location__icontains=farmer.district
            )

    class Meta:
        model = Produce
        fields = ['hub']
        widgets = {
            'hub': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        help_texts = {
            'hub': 'Select the nearest hub for your produce'
        }
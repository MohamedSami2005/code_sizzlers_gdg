from django import forms
from .models import Consumer

class ConsumerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = ['phone', 'address', 'pincode', 'city']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    payment_method = forms.ChoiceField(
        choices=[('COD', 'Cash on Delivery'), ('ONLINE', 'Online Payment')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='COD'
    )
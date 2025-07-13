from django import forms
from .models import OrderAddressInfo

class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = OrderAddressInfo
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'region', 'town_city', 'gps','address_1', 'address_2' ]

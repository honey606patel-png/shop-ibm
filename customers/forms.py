from django import forms
from .models import Customer, Order

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product_name', 'amount', 'status']


        
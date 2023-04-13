from django import forms

# import models
from .models import Sale

class ProcessSaleForm(forms.Form):
    
    payment_type = forms.ChoiceField(
        required=False,
        choices=Sale.PAYMENT_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field form-field prod-field',
            }
        )
    )
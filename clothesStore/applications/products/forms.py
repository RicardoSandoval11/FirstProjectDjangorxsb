from django import forms
from .models import Product, Category, Materials, Color



class CreateProductForm(forms.ModelForm):

    OFFER_CHOICES = (
            (True, 'Yes'),
            (False, 'No'),
        )
        

    is_offer= forms.ChoiceField(
        label='is_offer', 
        choices=OFFER_CHOICES, 
        widget=forms.Select(
            attrs={
                'class':'form-field prod-field',
            }
        )
    )


    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'composition',
            'price',
            'size',
            'colors',
            'image1',
            'image2',
            'image3',
            'stock',
            'category',
            'purchase_price',
            'offer_price', 
            'is_offer'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Name of the product',
                    'class': 'form-field prod-field'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Brief description of the product',
                    'class': 'form-field prod-field'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-field prod-field'
                }
            ),
            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-field prod-field'
                }
            ),
            'image1': forms.FileInput(
                attrs={
                    'class': 'form-field prod-field-img'
                }
            ),
            'image2': forms.FileInput(
                attrs={
                    'class': 'form-field prod-field-img'
                }
            ),
            'image3': forms.FileInput(
                attrs={
                    'class': 'form-field prod-field-img'
                }
            ),
            'composition': forms.SelectMultiple(
                attrs={
                    'class': 'form-field select-multiple prod-field'
                }
            ),
            'colors': forms.SelectMultiple(
                attrs={
                    'class': 'form-field select-multiple prod-field'
                }
            ),
            'size': forms.Select(
                attrs={
                    'class': 'form-field prod-field'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-field prod-field'
                }
            ),
            'purchase_price': forms.NumberInput(
                attrs={
                    'class': 'form-field prod-field'
                }
            ),
            'offer_price': forms.NumberInput(
                attrs={
                    'class': 'form-field prod-field'
                }
            )
        }
    # Validations

    def clean_offer_price(self):
        offer_price = self.cleaned_data['offer_price']
        print(self.cleaned_data)
        if hasattr(self.cleaned_data, 'is_offer'):
            if offer_price == None:
                raise forms.ValidationError('Please, enter an offer price if the product is in offer')
        return offer_price
    
    def clean_purchase_price(self):
        price = self.cleaned_data['price']
        purchase_price = self.cleaned_data['purchase_price']
        if purchase_price > price:
            raise forms.ValidationError('Sale price must be grater than purchase price')
        
        return purchase_price

class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
            'sex'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Hats',
                    'class': 'form-field register-field',
                }
            ),
            'sex':forms.Select(
                choices=Category.GENDER_CHOICES,
                attrs={
                    'class':'form-field register-field sex-field'
                }
            )
        }

class CreateProductMaterialForm(forms.ModelForm):

    class Meta:
        model = Materials
        fields = [
            'material'
        ]
        widgets = {
            'material': forms.TextInput(
                attrs={
                    'placeholder': 'Name of the material',
                    'class': 'form-field register-field',
                }
            )
        }

class CreateProductColorForm(forms.ModelForm):

    class Meta:
        model = Color
        fields = [
            'color'
        ]
        widgets = {
            'color': forms.TextInput(
                attrs={
                    'placeholder': 'Name of the color',
                    'class': 'form-field register-field',
                }
            )
        }


    

from django.db import models

from model_utils.models import TimeStampedModel

# managers
from .managers import (
    CategoriesManager, 
    ProductsByCategory,
    CarShopManager,
    WishListManager
)

# user model
from applications.users.models import User


class Color(TimeStampedModel):
    color = models.CharField(
        verbose_name='Color name',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
    
    def __str__(self):
        return self.color

class Materials(TimeStampedModel):
    material = models.CharField(
        verbose_name='Material name',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
    
    def __str__(self):
        return self.material

class Category(TimeStampedModel):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    name = models.CharField(
        verbose_name='Category name',
        max_length=100
    )
    sex = models.CharField(
        verbose_name='Sex',
        max_length=1,
        choices=GENDER_CHOICES
    )

    objects = CategoriesManager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name +' - '+ self.sex

class Product(models.Model):

    SIZE_CHOICES = [
        ('1', 'XS'),
        ('2', 'S'),
        ('3', 'M'),
        ('4', 'L'),
        ('5', 'XL'),
    ]

    name = models.CharField(
        verbose_name='Name',
        max_length=100, 
        unique=True
    )
    description = models.TextField(
        verbose_name='Description',
        max_length=200
    )
    composition = models.ManyToManyField(Materials)
    price = models.PositiveIntegerField(
        'Sale price',
    )
    size = models.CharField(
        verbose_name='Size',
        max_length=1,
        choices=SIZE_CHOICES
    )
    colors = models.ManyToManyField(Color)
    image1 = models.ImageField(
        verbose_name='image 1',
        upload_to='products/'
    )
    image2 = models.ImageField(
        verbose_name='Image 2',
        upload_to='products/'
    )
    image3 = models.ImageField(
        verbose_name='Image 3',
        upload_to='products/'
    )
    stock = models.PositiveIntegerField(
        verbose_name='Stock'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    is_offer = models.BooleanField(
        'Is offer?',
        blank=True
    )
    purchase_price = models.PositiveIntegerField(
        'Purchase price',
    )
    offer_price = models.PositiveIntegerField(
        'offer price',
        default=0.00
    )

    objects = ProductsByCategory()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return str(self.id) + ' - ' +self.name

class CarShop(TimeStampedModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Product',
        related_name='product_car'
    )
    amout_product = models.PositiveIntegerField('Number of products')
    total_amount = models.FloatField('Amount')

    objects = CarShopManager()

    class Meta:
        verbose_name = 'Car shop'
        verbose_name_plural = 'Car shop'
        ordering = ['-created']
    
    def __str__(self):
        return str(self.product.name)
    
class WishList(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Product',
        related_name='product_wish_list'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='wish_prod_user'
    )

    objects = WishListManager()

    class Meta:
        unique_together = [['product', 'user']]
        verbose_name = 'Wish product'
        verbose_name_plural = 'Wish products'
    
    def __str__(self):
        return str(self.id) +' - '+self.product.name +' - '+self.user.email

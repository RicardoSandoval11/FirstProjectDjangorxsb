from django.db import models
from model_utils.models import TimeStampedModel

# import required models
from applications.users.models import User
from applications.products.models import Product

# import managers
from .managers import SaleDetailsManager, SaleManager


class Sale(TimeStampedModel):
    """ Model to show the summary of a sale """

    # Payment options
    CARD = '0'
    CASH = '1'
    OTHER = '2'

    PAYMENT_CHOICES = [
        (CARD, 'Credit card'),
        (CASH, 'Cash'),
        (OTHER, 'Other')
    ]

    sale_date = models.DateTimeField(
        'Sale date',
    )
    amount = models.DecimalField(
        'Amount',
        max_digits=5,
        decimal_places=2
    )
    payment_type = models.CharField(
        'Payment type',
        max_length=1,
        choices=PAYMENT_CHOICES
    )
    total_revenue = models.DecimalField(
        'Total revenue',
        max_digits=5,
        decimal_places=2
    )

    objects = SaleManager()

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        return 'N ['+ str(self.id) +'] - Amount: '+ str(self.amount)

class DetailsSale(TimeStampedModel):
    """ model to register each product of a sale """
    product_name = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        verbose_name='product',
        related_name='product_sale'
    )
    amount = models.PositiveIntegerField('Amount')
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        verbose_name='Code sale',
        related_name='detail_sale'
    )
    price_sale = models.DecimalField(
        'Price sale',
        max_digits=5,
        decimal_places=2
    )
    purchase_price = models.DecimalField(
        'Purchase price',
        max_digits=5,
        decimal_places=2
    )
    revenue = models.DecimalField(
        'Revenue',
        max_digits=5,
        decimal_places=2
    )

    objects = SaleDetailsManager()

    class Meta:
        verbose_name = 'Sale detail'
        verbose_name_plural = 'Sale details'

    def __str__(self):
        return 'Product name: '+str(self.product_name)+' - Amount: '+str(self.amount)+' - Revenue: '+str(self.revenue)


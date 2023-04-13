from django.db import models

# to calculate total amount
from django.db.models import F, FloatField, Sum

class CategoriesManager(models.Manager):
    
    def get_categories(self, sex):
        return self.filter(
            sex=sex
        ).order_by('name')

# Managerws to retrieve products
class ProductsByCategory(models.Manager):
    
    def get_products_by_category_keyword(self, category_id, keyword):
        return self.filter(
            category=category_id,
            name__icontains=keyword
        ).order_by('name')
    
    def get_out_of_stock_products(self):
        return self.filter(
            stock=0
        ).order_by('name')

# Managers to retrieve products in carshop
class CarShopManager(models.Manager):

    def get_products_by_user(self, user_id):
        return self.filter(
            user__id=user_id
        ).order_by('-created')
    
    def get_total_shop(self):

        amount_total = self.aggregate(
            total=Sum(
                F('total_amount'),
                output_field=FloatField()
            ),
        )
        return amount_total['total']

class WishListManager(models.Manager):

    def get_wish_list_prod_by_user(self, user_id):
        return self.filter(
            user__id=user_id
        )
from django.db import models
from django.db.models import Max, Sum

class SaleDetailsManager(models.Manager):

    def get_detail_sales_by_sale(self, sale_obj):
        return self.filter(
            sale=sale_obj
        ).order_by('-created')

class SaleManager(models.Manager):

    def get_sales_by_date_range(self, start_date, end_date):
        return self.filter(
            sale_date__range=(start_date, end_date)
        ).order_by('-created')
    
    def get_max_sale(self, start_date, end_date):
        highest_sale = self.filter(
            sale_date__range=(start_date, end_date)
        ).aggregate(highest_sale=Max('amount'))['highest_sale']
        return highest_sale
    
    def get_total_revenue_of_month(self, start_date, end_date):
        total_revenue = self.filter(
            sale_date__range=(start_date, end_date)
        ).aggregate(total_revenue= Sum('total_revenue'))
        return total_revenue
    

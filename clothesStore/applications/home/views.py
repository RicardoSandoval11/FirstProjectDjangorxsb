import datetime

from django.shortcuts import render
from django.views.generic import TemplateView

# product's models
from applications.products.models import Category

# import external models
from applications.users.models import User
from applications.sales.models import Sale
from applications.products.models import Product

# Permissions
from applications.users.mixins import AdminPermissionMixin, WorkerPermissionMixin

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['women_categories'] = Category.objects.get_categories('F')
        context['men_categories'] = Category.objects.get_categories('M')
        return context

class PanelView(AdminPermissionMixin,TemplateView):
    template_name = 'home/panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get active users
        context['active_users'] = User.objects.filter(is_active=True).count()

        # get out of stock products
        context['out_of_stock'] = Product.objects.filter(stock=0).count()

        start_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
        end_date = start_date - datetime.timedelta(days=30)
        start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()

        # Get highest sale of the month
        context['highest_sale'] = Sale.objects.get_max_sale(end_date, start_date)

        # Get total sales of the month
        context['total_sales'] = Sale.objects.get_sales_by_date_range(end_date, start_date).count()

        # Get total revenue of the month
        context['total_revenue'] = Sale.objects.get_total_revenue_of_month(end_date, start_date)['total_revenue']

        return context

class DashboardPanelview(WorkerPermissionMixin, TemplateView):
    template_name = 'home/dashboard.html'
import datetime

from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# import required models
from applications.products.models import CarShop, Product
from applications.sales.models import Sale, DetailsSale

# import forms
from .forms import ProcessSaleForm


from django.views.generic import ListView, FormView, DeleteView, DetailView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# Permissions
from applications.users.mixins import ClientPermissionMixin, AdminPermissionMixin, WorkerPermissionMixin


class CarShopProdListView(LoginRequiredMixin,ListView):

    template_name = 'sales/car_shop.html'
    context_object_name = 'sales'
    login_url = 'users_app:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not CarShop.objects.get_products_by_user(self.request.user.id):
            context['products'] = False
        else:
            context['products'] = True

        return context
    
    def get_queryset(self):
        """ Return the products in carshop of a specific user """
        products = CarShop.objects.get_products_by_user(self.request.user.id)
        for car_product in products:
            product= Product.objects.get(id=car_product.product.id)
            if(car_product.amout_product > product.stock):
                car_product.amout_product = product.stock
            product.save()

        return products
    
class ProcessSale(LoginRequiredMixin,FormView):

    template_name = 'sales/complete_sale.html'
    form_class = ProcessSaleForm
    success_url = '.'

    def form_valid(self, form):
        payment_type = form.cleaned_data['payment_type']
        # Getting all products in carshop of user
        car_products = CarShop.objects.get_products_by_user(self.request.user.id)

        # create Sale object
        sale = Sale.objects.create(
            sale_date = timezone.now(),
            amount = 0,
            payment_type = payment_type,
            total_revenue = 0
        )

        sale_details = []

        for car_product in car_products:
            sale_detail = DetailsSale(
                product_name = car_product.product,
                amount = car_product.amout_product,
                sale = sale,
                price_sale = car_product.total_amount,
                purchase_price = car_product.product.purchase_price*car_product.amout_product,
                revenue = car_product.total_amount - car_product.product.purchase_price*car_product.amout_product
            )
            # saving sale details
            sale_details.append(sale_detail)

            # updating amount of the product
            product = Product.objects.get(
                id=car_product.product.id
            )
            if( product.stock >= car_product.amout_product):
                product.stock = product.stock - car_product.amout_product
            else:
                product.stock = 0
            product.save()

            # increasing the total amount of sale and total revenue
            sale.amount = sale.amount + car_product.total_amount
            sale.total_revenue = sale.total_revenue + car_product.total_amount - car_product.product.purchase_price*car_product.amout_product
        
        # saving the sale
        sale.save()

        # saving the details of the sale
        DetailsSale.objects.bulk_create(sale_details)

        # Removing products from car shop
        car_products.delete()

        return HttpResponseRedirect(
                reverse(
                    'sales_app:sale-datails',
                    kwargs={'pk': sale.pk },
                )
            )
    
class ShowSaleView(LoginRequiredMixin,DetailView):
    template_name = 'sales/sale.html'
    model = Sale
    context_object_name = 'sale'

class DeleteSale(AdminPermissionMixin,DeleteView):
    model = Sale
    success_url = reverse_lazy('sales_app:sales')

class ShowAllSalesView(WorkerPermissionMixin,ListView):
    template_name = 'sales/all_sales.html'
    context_object_name = 'sales'
    model = Sale
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not Sale.objects.all():
            context['products'] = False
        else:
            context['products'] = True
        return context
    
    def get_queryset(self):

        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            sales = Sale.objects.get_sales_by_date_range(start_date, end_date)
        else:
            sales = Sale.objects.all()
        return sales

class ShowDetailsSaleView(WorkerPermissionMixin,ListView):

    template_name = 'sales/sale_details.html'
    context_object_name = 'sales'
    
    def get_queryset(self):
        sale = Sale.objects.get(id=self.kwargs['pk'])
        sales = DetailsSale.objects.get_detail_sales_by_sale(sale)    
        return sales



from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView, 
    DetailView, 
    DeleteView,
    UpdateView,
    View,
    CreateView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

#models
from .models import Product, CarShop, WishList, Color

# Permissions
from applications.users.mixins import WorkerPermissionMixin, AdminPermissionMixin

#forms
from .forms import  (
    CreateProductForm, 
    CreateCategoryForm, 
    CreateProductMaterialForm, 
    CreateProductColorForm
)


class ProductsByCategoryView(ListView):
    """ Show products by category and filter the results by keyword """

    template_name='products/products_by_category.html'
    context_object_name = 'products'
    paginate_by = 5
   
    def get_queryset(self):
        kword = self.request.GET.get('keyword', '')
        category_id = self.kwargs['pk']
        filtered_objects = Product.objects.get_products_by_category_keyword(category_id, kword)     
        return filtered_objects

class ProductDetailsView(DetailView):
    """ Show details of each product """

    template_name = 'products/product.html'
    model = Product
    context_object_name='product'

class ProductDeleteConfirmatioView(AdminPermissionMixin,DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url= '/'

class UpdateProductInfoView(WorkerPermissionMixin,UpdateView):
     model = Product
     template_name = 'products/update_product.html'
     success_url = reverse_lazy('home_app:home')
     form_class = CreateProductForm

class ListOfferProductsView(ListView):
    template_name = 'products/offer_products.html'
    context_object_name = 'offer_products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not Product.objects.filter(is_offer=True):
            context['areThereProducts'] = False
        else:
            context['areThereProducts'] = True

        return context

    def get_queryset(self):
        return Product.objects.filter(
            is_offer=True
        )

class CreateProductView(WorkerPermissionMixin,CreateView):
    template_name = 'products/create_product.html'
    form_class = CreateProductForm
    success_url = reverse_lazy('products_app:offer-products')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class AddToCarView(LoginRequiredMixin, View):

    login_url = 'users_app:login'

    """ Add a product to car """
    def post(self, request, *args, **kwargs):

        product = Product.objects.get(
            id=self.kwargs['pk']
        )

        if(product.is_offer):
            price = product.offer_price
        else:
            price = product.price

        car, created = CarShop.objects.get_or_create(
            product=product,
            defaults={
                'user':request.user,
                'product':product,
                'amout_product':1,
                'total_amount':price
            }
            )

        if(not created):
            car.amout_product = car.amout_product + 1
            if(product.is_offer):
                car.total_amount = car.total_amount + product.offer_price
            else:
                car.total_amount = car.total_amount + product.price
            car.save()

        return HttpResponseRedirect(
            reverse(
            'sales_app:car-shop'
            )
        )    
    

class RemoveFromCarView(LoginRequiredMixin, View):

    login_url = 'users_app:login'

    """ Remove products from carshop """

    def post(self, request, *args, **kwargs):
        car = CarShop.objects.get(id=self.kwargs['pk'])
        if car.amout_product >= 1:
            car.amout_product = car.amout_product - 1
            if(car.product.is_offer):
                car.total_amount = car.total_amount - car.product.offer_price
            else:
                car.total_amount = car.total_amount - car.product.price

            if car.amout_product == 0:
                car.delete()
                return HttpResponseRedirect(
                    reverse(
                    'home_app:home'
                    )
                )
            else:
                car.save()
        
        return HttpResponseRedirect(
            reverse(
                'sales_app:car-shop'
            )
        )
            
class WishListView(LoginRequiredMixin, ListView):

    login_url = 'users_app:login'

    template_name = 'products/wish_list.html'
    paginate_by = 5
    context_object_name = 'wish_list_products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        if not WishList.objects.get_wish_list_prod_by_user(self.request.user.id):
            context['products'] = False
        else:
            context['products'] = True
        return context

    def get_queryset(self):
        wish_products = WishList.objects.get_wish_list_prod_by_user(self.request.user.id)
        return wish_products

class RemoveFromWishListView(LoginRequiredMixin, DeleteView):
    login_url = 'users_app:login'
    model = WishList
    success_url= reverse_lazy('products_app:wish-list')

# register a product in wish list
class AddProductWishListView(LoginRequiredMixin, View):

    login_url = 'users_app:login'

    def post(self, request, *args, **kwargs):

        product = Product.objects.get(
            id=self.kwargs['pk']
        )

        WishList.objects.get_or_create(
            product=product,
            defaults={
                'user':self.request.user,
                'product':product
            }
            )

        return HttpResponseRedirect(
            reverse(
                'products_app:wish-list'
            )
        )

class GetOutOfStockProducts(WorkerPermissionMixin,ListView):

    template_name = 'products/out_stock_prod.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        if not Product.objects.get_out_of_stock_products():
            context['is_products'] = False
        else:
            context['is_products'] = True
        return context

    def get_queryset(self):
        out_of_stock_products= Product.objects.get_out_of_stock_products()
        return out_of_stock_products

class AddProductView(WorkerPermissionMixin,TemplateView):
    template_name = 'products/add_product.html'

class CreateCategoryView(WorkerPermissionMixin,CreateView):
    template_name = 'products/create_category.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('products_app:add-new-product')

class CreateProductMaterialView(WorkerPermissionMixin,CreateView):
    template_name = 'products/create_material.html'
    form_class = CreateProductMaterialForm
    success_url = reverse_lazy('products_app:add-new-product')

class CreateProductColorView(WorkerPermissionMixin,CreateView):
    template_name = 'products/create_color.html'
    form_class = CreateProductColorForm
    success_url = reverse_lazy('products_app:add-new-product')



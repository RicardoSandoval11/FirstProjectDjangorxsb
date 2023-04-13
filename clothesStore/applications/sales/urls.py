from django.urls import path

# import views
from .views import (
    CarShopProdListView, 
    ShowSaleView, 
    ProcessSale, 
    ShowAllSalesView, 
    ShowDetailsSaleView,
    DeleteSale
)

app_name = 'sales_app'

urlpatterns = [
    path(
    'carshop/',
    CarShopProdListView.as_view(),
    name='car-shop'
    ),
    path(
    'process-sale/',
    ProcessSale.as_view(),
    name='process-sale'
    ),
    path(
    'sale-datails/<pk>',
    ShowSaleView.as_view(),
    name='sale-datails'
    ),
    path(
    'sales/',
    ShowAllSalesView.as_view(),
    name='sales'
    ),
    path(
    'details-sale/<pk>',
    ShowDetailsSaleView.as_view(),
    name='detail-sales'
    ),
    path(
    'delete-sale/<pk>',
    DeleteSale.as_view(),
    name='delete-sale'
    ),
]


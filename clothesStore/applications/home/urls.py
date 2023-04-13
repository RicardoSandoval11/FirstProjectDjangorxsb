from django.urls import path

# Views
from .views import HomeView, PanelView, DashboardPanelview

app_name='home_app'

urlpatterns = [
    path(
        '', 
        HomeView.as_view(), 
        name='home'
    ),
    path(
        'admin-panel/', 
        PanelView.as_view(), 
        name='admin-panel'
    ),
    path(
        'worker-panel/', 
        DashboardPanelview.as_view(), 
        name='worker-panel'
    ),
]
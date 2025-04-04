from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='admin_dashboard'),
    
    # User Management
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('farmers/verify/<int:farmer_id>/', views.verify_farmer, name='verify_farmer'),
    path('consumers/', views.consumer_list, name='consumer_list'),
    
    # Hub Management
    path('hubs/', views.manage_hubs, name='manage_hubs'),
    path('hubs/add/', views.add_hub, name='add_hub'),
    path('hubs/edit/<int:hub_id>/', views.edit_hub, name='edit_hub'),
    
    # Dispute Resolution
    path('disputes/', views.dispute_list, name='dispute_list'),
    path('disputes/resolve/<int:dispute_id>/', views.resolve_dispute, name='resolve_dispute'),
    
    # Reports
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
]
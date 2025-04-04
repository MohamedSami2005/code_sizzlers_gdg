from django.urls import path
from . import views

urlpatterns = [
    # Farmer Dashboard
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('hubs/create/', views.create_hub, name='create_hub'),
    path('hubs/<int:hub_id>/', views.hub_detail, name='hub_detail'),
    path('hubs/', views.hub_list, name='hub_list'),
    # Produce Management
    path('add-produce/', views.add_produce, name='add_produce'),
    path('edit-produce/<int:pk>/', views.edit_produce, name='edit_produce'),
    path('delete-produce/<int:pk>/', views.delete_produce, name='delete_produce'),
    
    # Hub Management
    path('hubs/', views.hub_list, name='hub_list'),
    path('hub/<int:hub_id>/', views.hub_dashboard, name='hub_dashboard'),
    path('submit-to-hub/<int:produce_id>/', views.submit_to_hub, name='submit_to_hub'),
    
    # Farmer Registration
    path('register/', views.farmer_register, name='farmer_register'),
    
    # Profile Management
    path('profile/', views.farmer_profile, name='farmer_profile'),
]
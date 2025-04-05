from django.urls import path
from . import views

urlpatterns = [
    # Marketplace
    path('', views.marketplace, name='marketplace'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('market/', views.marketplace, name='marketplace'),
    
    # Cart & Orders
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:produce_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    
    # Consumer Registration
    path('register/', views.consumer_register, name='consumer_register'),
]
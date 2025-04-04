"""
URL configuration for uzhavan_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from uzhavan_hub import views as hub_views
from consumer_app import views as consumer_views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Farmer/Hub URLs
    path('', hub_views.home, name='home'),
    path('hub/', include('uzhavan_hub.urls')),
    
    # Consumer URLs
    path('market/', include('consumer_app.urls')),
    
    # Admin Panel URLs
    path('uzhavan-admin/', include('admin_panel.urls')),
    
    # Password Reset URLs (for future use)
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
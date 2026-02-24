from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    
    path('buy/<int:product_id>/<int:pickup_point_id>/', views.create_order, name='create_order'),
    
    path('manage-users/', views.manage_users, name='manage_users'),
]

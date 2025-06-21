from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.products, name='products'),
    path('negotiate/', views.negotiate, name='negotiate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('handle-login/', views.handle_login, name='handle_login'),
    path('handle-register/', views.handle_register, name='handle_register'),
    path('handle_login/', views.handle_login, name="handle_login"),
    path("logout/", views.logout_view, name="logout"),
    path("get_products/", views.get_products, name="get_products"),
    path("add_product/", views.add_product, name="add_product"),
    path("edit_product/", views.edit_product, name="edit_product"),
    path("delete_product/", views.delete_product, name="delete_product"),
    path("purchase_product/", views.purchase_product, name="purchase_product"),
    path("get_negotiate_products/", views.negotiate_products, name="get_negotiate_products"),
]

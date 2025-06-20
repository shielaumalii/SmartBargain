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
]

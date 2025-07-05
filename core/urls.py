from django.urls import path, include
from . import views
from .backend.dashboard import get_orders


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.products, name='products'),
    path('negotiate/', views.negotiate, name='negotiate'),
    path('login/', views.login_view, name='login'),
    path('handle-login/', views.handle_login, name='handle_login'),
    path('handle-register/', views.handle_register, name='handle_register'),
    path("logout/", views.logout_view, name="logout"),
    path("get_products/", views.get_products, name="get_products"),
    path("add_product/", views.add_product, name="add_product"),
    path("edit_product/", views.edit_product, name="edit_product"),
    path("delete_product/", views.delete_product, name="delete_product"),
    path("purchase_product/", views.purchase_product, name="purchase_product"),
    path("get_negotiate_products/", views.negotiate_products, name="get_negotiate_products"),
    path('save_bargain_setting/', views.save_bargain_setting, name='save_bargain_setting'),
    path('save_bargain_request/', views.save_bargain_request, name='save_bargain_request'),
    path("get_negotiation_tasks/", views.get_negotiation_tasks_view, name="get_negotiation_tasks"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("submit_negotiation_response/", views.submit_negotiation_response, name="submit_negotiation_response"),
    path("get_negotiation_dashboard/", views.get_negotiation_dashboard, name="get_negotiation_dashboard"),
    path("update_negotiation_dashboard/", views.update_negotiation_dashboard, name="update_negotiation_dashboard"),
    #Contact us
    path('submit_contact_message/', views.submit_contact_message, name='submit_contact_message'),
    path('get_contact_messages/', views.get_contact_messages, name='get_contact_messages'),
    path('close_contact_message/', views.close_contact_message, name='close_contact_message'),
    #Dashbaord Orders
    path('get_orders/', get_orders, name='get_orders'),


    


    # path('', include('core.urls')),
]

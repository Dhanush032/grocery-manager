from django.urls import path
from . import views

urlpatterns = [
    path('getProducts/', views.get_products),
    path('getUOM/', views.get_uom),
    path('insertProduct/', views.insert_product),
    path('deleteProduct/', views.delete_product),
    path('updateProduct/', views.update_product),
    path('insertUOM/', views.insert_uom),
    path('getAllOrders/', views.get_all_orders),
    path('insertOrder/', views.insert_order),
    path('getOrderDetails/<int:order_id>/', views.get_order_details),

]


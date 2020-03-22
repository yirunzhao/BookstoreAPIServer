from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_carts),
    path('delete/', views.delete_book),
    path('modify/', views.modify_book_count),
    path('add/', views.add_book),
    path('commit/', views.generate_orders),
    path('purchase/', views.purchase),
    path('history/', views.get_history)
]

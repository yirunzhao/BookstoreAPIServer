from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_book),
    path('category/', views.select_category),
    path('comment/', views.comment),
    path('one/', views.get_one_book)
]

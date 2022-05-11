from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('customer/', views.customer),
    path('customer/<str:pk>' ,views.customer, name="customer"),
    path('books/', views.books, name="books"),
    path('profile/', views.profile, name="profile"),
    # path('create/', views.create, name="create"),
    path('create/<str:pk>', views.create, name="create"),
    path('update/<str:pk>', views.update, name="update"),
    path('delete/<str:pk>', views.delete, name="delete"),
]




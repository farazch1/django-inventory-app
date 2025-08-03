# # example/urls.py
# from django.urls import path

# from example.views import index


# urlpatterns = [
#     path('', index),
# ]

from django.urls import path
from .views import inventory_view

urlpatterns = [
    path('', inventory_view, name='inventory'),
]
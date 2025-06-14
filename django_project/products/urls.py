from django.urls import path

from .views import ProductListView, ProductDetails

urlpatterns = [
    path("<slug:slug>/", ProductDetails.as_view(), name="product_details"),
    path("", ProductListView.as_view(), name="product_list"),
]

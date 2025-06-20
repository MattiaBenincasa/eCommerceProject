from django.urls import path, include
from .views import ProductListView, ProductDetails, add_review

urlpatterns = [
    path("<slug:slug>/", ProductDetails.as_view(), name="product_details"),
    path("", ProductListView.as_view(), name="product_list"),
    path('cart/cart/', include("cart.urls"), name="cart"),
    path("products/<slug:product_slug>/add_review/", add_review, name="add_review"),
]

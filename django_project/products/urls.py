from django.urls import path, include
from .views import (
    ProductListView,
    ProductDetails,
    add_review,
    AddProduct,
    DeleteProduct,
    UpdateProduct,
    AddCategory,
    DeleteCategory,
    UpdateCategory,
    CategoriesList,
    DeleteReview,
)

urlpatterns = [
    path("add_product/", AddProduct.as_view(), name="add_product"),
    path("update_product/<int:pk>", UpdateProduct.as_view(), name="update_product"),
    path("delete_product/<int:pk>", DeleteProduct.as_view(), name="delete_product"),
    path("categories_list/", CategoriesList.as_view(), name='categories_list'),
    path("add_category/", AddCategory.as_view(), name="add_category"),
    path("delete_category/<int:pk>", DeleteCategory.as_view(), name="delete_category"),
    path("update_category/<int:pk>", UpdateCategory.as_view(), name="update_category"),
    path("", ProductListView.as_view(), name="product_list"),
    path("delete_review/<int:pk>", DeleteReview.as_view(), name="delete_review"),
    path("<slug:product_slug>/add_review/", add_review, name="add_review"),
    path("<slug:slug>/", ProductDetails.as_view(), name="product_details"),
]

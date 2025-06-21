from django.urls import path
from .views import (
    AddressListView,
    AddressCreateView,
    AddressUpdateView,
    AddressDeleteView,
)


urlpatterns = [
    path('', AddressListView.as_view(), name='address_list'),
    path('add/', AddressCreateView.as_view(), name='address_add'),
    path('<int:pk>/edit/', AddressUpdateView.as_view(), name='address_edit'),
    path('<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),
]

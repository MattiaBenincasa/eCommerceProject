from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include("products.urls")),
    path('accounts/', include("accounts.urls")),
    path('cart/', include("cart.urls")),
    path('orders/', include("orders.urls")),
    path('addresses/', include("addresses.urls")),
    path('', include("pages.urls"))
]

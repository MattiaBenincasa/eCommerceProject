from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include("products.urls")),
    path('accounts/', include("accounts.urls")),
    path('cart/', include("cart.urls")),
    path('orders/', include("orders.urls")),
    path('addresses/', include("addresses.urls")),
    path('checkout/', include("checkout.urls")),
    path('', include("pages.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

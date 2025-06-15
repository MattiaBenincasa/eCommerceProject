from django.views.generic import TemplateView
from products.models import Product
from products.forms import ProductSearchForm


class HomePageView(TemplateView):
    template_name = 'HomePage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductSearchForm(self.request.GET)
        context['latest_products'] = Product.objects.filter(stock__gt=0).order_by('-created_at')[:4]
        return context



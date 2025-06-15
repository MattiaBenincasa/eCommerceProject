from django.views.generic import ListView, DetailView
from .models import Product
from .forms import ProductSearchForm
from django.db.models import Q


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductSearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data.get('q')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)  # Ricerca per nome o descrizione
                ).distinct()  # Evita duplicati se un prodotto corrisponde a più condizioni

            categories = form.cleaned_data.get('category')
            if categories:
                queryset = queryset.filter(category__in=categories)

            available_only = form.cleaned_data.get('available_only')
            if available_only:
                queryset = queryset.filter(stock__gt=0)

            sort_by = form.cleaned_data.get('sort_by')
            if sort_by:
                if sort_by == 'name_asc':
                    queryset = queryset.order_by('name')
                elif sort_by == 'name_desc':
                    queryset = queryset.order_by('-name')
                elif sort_by == 'price_asc':
                    queryset = queryset.order_by('price')
                elif sort_by == 'price_desc':
                    queryset = queryset.order_by('-price')

        if not queryset.ordered:
            queryset = queryset.order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductSearchForm(self.request.GET)
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = "product_details.html"

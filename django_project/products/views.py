from django.views.generic import ListView, DetailView
from .models import Product, Category
from .forms import ProductSearchForm  # Importa il tuo form di ricerca
from django.db.models import Q  # Per query complesse (es. OR per la ricerca)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductSearchForm(self.request.GET)

        if form.is_valid():
            # 1. Filtro per termine di ricerca (q)
            query = form.cleaned_data.get('q')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)  # Ricerca per nome o descrizione
                ).distinct()  # Evita duplicati se un prodotto corrisponde a più condizioni

            # 2. Filtro per categoria
            categories = form.cleaned_data.get('category')
            if categories:  # categories sarà un queryset di oggetti Category
                # Filtra i prodotti la cui categoria è tra quelle selezionate
                queryset = queryset.filter(category__in=categories)

            # 3. Filtro per disponibilità (quantity > 0)
            available_only = form.cleaned_data.get('available_only')
            if available_only:
                queryset = queryset.filter(stock__gt=0)  # quantity > 0

            # 4. Ordinamento
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

        # Ordine predefinito se nessun ordinamento è stato specificato o se il form non è valido
        # Questo previene l'errore se non c'è un ordine definito e la paginazione è attiva
        if not queryset.ordered:
            queryset = queryset.order_by('name')  # Ordine predefinito per nome

        return queryset

    def get_context_data(self, **kwargs):
        """
        Passa il form di ricerca al template.
        """
        context = super().get_context_data(**kwargs)
        # Passa un'istanza del form, pre-popolata con i dati GET se presenti
        context['form'] = ProductSearchForm(self.request.GET)
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = "product_details.html"

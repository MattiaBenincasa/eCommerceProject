from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Product, Review
from .forms import ProductSearchForm, ProductReviewForm
from orders.models import OrderItem
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
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object() # Ottiene il prodotto corrente

        # Recensioni esistenti per questo prodotto
        context['reviews'] = Review.objects.filter(product=product)

        context['review_form'] = None # Inizializza il form a None
        context['has_purchased'] = False
        context['user_review'] = None # Recensione dell'utente corrente, se esiste

        if self.request.user.is_authenticated:
            # Controlla se l'utente ha acquistato il prodotto
            context['has_purchased'] = OrderItem.objects.filter(
                order__customer=self.request.user,
                product=product,
                order__status='Delivered' # L'utente può recensire solo se l'ordine è stato consegnato
            ).exists()

            # Controlla se l'utente ha già recensito questo prodotto
            user_review = Review.objects.filter(
                customer=self.request.user,
                product=product
            ).first()

            if user_review:
                context['user_review'] = user_review
                # Se l'utente ha già recensito, il form è pre-popolato
                context['review_form'] = ProductReviewForm(instance=user_review)
            elif context['has_purchased']: # Se non ha recensito ma ha acquistato e ordine consegnato, mostra il form vuoto
                context['review_form'] = ProductReviewForm()
            # else: l'utente non può recensire (non ha acquistato o non è loggato o ordine non consegnato)

        return context


@login_required
def add_review(request, product_slug):
    """
    Permette a un utente di aggiungere o modificare una recensione a un prodotto.
    L'utente deve essere loggato e aver acquistato il prodotto con ordine consegnato.
    """
    product = get_object_or_404(Product, slug=product_slug)

    # 1. Verifica se l'utente ha acquistato il prodotto e l'ordine è stato consegnato
    has_purchased_and_delivered = OrderItem.objects.filter(
        order__customer=request.user,
        product=product,
        order__status='Delivered'
    ).exists()

    if not has_purchased_and_delivered:
        messages.error(request, "Puoi recensire solo prodotti che hai acquistato e che sono stati consegnati.")
        return redirect('product_details', slug=product.slug)

    # 2. Controlla se l'utente ha già recensito questo prodotto
    existing_review = Review.objects.filter(
        customer=request.user,
        product=product
    ).first()

    if request.method == 'POST':
        if existing_review:
            form = ProductReviewForm(request.POST, instance=existing_review) # Modifica la recensione esistente
        else:
            form = ProductReviewForm(request.POST) # Crea una nuova recensione

        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.product = product
            review.save()
            if existing_review:
                messages.success(request, "La tua recensione è stata modificata con successo!")
            else:
                messages.success(request, "La tua recensione è stata aggiunta con successo!")
            return redirect('product_details', slug=product.slug)
        else:
            messages.error(request, "Errore durante l'invio della recensione. Controlla il titolo e il commento.")
            # Se il form non è valido, puoi reindirizzare alla pagina del prodotto
            # e ProductDetails gestirà la ri-visualizzazione del form con gli errori.
            return redirect('product_details', slug=product.slug)
    else:
        # Se la richiesta non è POST, reindirizza alla pagina del prodotto
        return redirect('product_details', slug=product.slug)
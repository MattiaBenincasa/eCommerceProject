from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from .models import Product, Review, Category
from .forms import ProductSearchForm, ProductReviewForm, ProductForm, CategoryForm
from orders.models import OrderItem
from django.db.models import Q


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'product_list'

    def get_template_names(self):
        user = self.request.user
        if user.groups.filter(name='store_manager').exists():
            return 'store_manager/catalogue.html'
        else:
            return 'product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductSearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data.get('search_bar')
            categories = form.cleaned_data.get('category')
            availability = form.cleaned_data.get('availability')
            sort_by = form.cleaned_data.get('sort_by')

            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)
                ).distinct()

            if categories:
                queryset = queryset.filter(category__in=categories)

            if availability:
                if availability == 'available_only':
                    queryset = queryset.filter(stock__gt=0)
                elif availability == 'unavailable_only':
                    queryset = queryset.filter(stock=0)

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
        context['search_params'] = self.request.GET.urlencode()
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context['reviews'] = Review.objects.filter(product=product)

        context['review_form'] = None
        context['has_purchased'] = False
        context['user_review'] = None
        context['search_params_for_back_link'] = self.request.GET.urlencode()

        if self.request.user.is_authenticated:
            context['has_purchased'] = OrderItem.objects.filter(
                order__customer=self.request.user,
                product=product,
                order__status='Delivered'   # L'utente può recensire solo se l'ordine è stato consegnato
            ).exists()

            user_review = Review.objects.filter(
                customer=self.request.user,
                product=product
            ).first()

            if user_review:
                context['user_review'] = user_review
                context['review_form'] = ProductReviewForm(instance=user_review)
            elif context['has_purchased']:      # Se non ha recensito ma ha acquistato e ordine consegnato, mostra il form vuoto
                context['review_form'] = ProductReviewForm()

        return context


@permission_required('products.add_review')
@login_required
def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    has_purchased_and_delivered = OrderItem.objects.filter(
        order__customer=request.user,
        product=product,
        order__status='Delivered'
    ).exists()

    if not has_purchased_and_delivered:
        messages.error(request, "Puoi recensire solo prodotti che hai acquistato e che sono stati consegnati.")
        return redirect('product_details', slug=product.slug)

    existing_review = Review.objects.filter(
        customer=request.user,
        product=product
    ).first()

    if request.method == 'POST':
        if existing_review:
            form = ProductReviewForm(request.POST, instance=existing_review)
        else:
            form = ProductReviewForm(request.POST)

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
            return redirect('product_details', slug=product.slug)
    else:
        return redirect('product_details', slug=product.slug)


class DeleteReview(DeleteView, LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin):
    model = Review
    template_name = 'review_delete_confirm.html'
    context_object_name = 'review'
    permission_required = 'products.delete_review'
    __product_slug = ''

    def form_valid(self, form):
        self.__product_slug = self.get_object().product.slug
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'La tua recensione è stata eliminata con successo.')
        return reverse_lazy('product_details', kwargs={'slug': self.__product_slug})

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.customer

    def handle_no_permission(self):
        messages.error(self.request, 'Non hai il permesso di eliminare questa recensione.')
        return redirect('product_details', product_slug=self.get_object().product.slug)

# store manager views


class AddProduct(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    model = Product
    permission_required = 'products.add_product'
    template_name = 'store_manager/products_management.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('product_details', kwargs={'slug': self.object.slug})


class DeleteProduct(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Product
    permission_required = 'products.delete_product'
    template_name = 'product_delete_confirm.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')


class UpdateProduct(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Product
    permission_required = 'products.change_products'
    template_name = 'store_manager/products_management.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('product_details', kwargs={'slug': self.object.slug})


class CategoriesList(ListView, PermissionRequiredMixin):
    model = Category
    template_name = 'store_manager/categories_list.html'
    context_object_name = 'categories'
    permission_required = 'products.view_category'


class AddCategory(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    model = Category
    permission_required = 'products.add_category'
    template_name = 'store_manager/categories_management.html'
    form_class = CategoryForm
    success_url = reverse_lazy('categories_list')


class DeleteCategory(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Category
    permission_required = 'store_manager/products.delete_category'
    template_name = 'store_manager/delete_category_confirm.html'
    context_object_name = 'category'
    success_url = reverse_lazy('categories_list')


class UpdateCategory(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Category
    permission_required = 'products.change_category'
    template_name = 'store_manager/categories_management.html'
    context_object_name = 'category'
    form_class = CategoryForm
    success_url = reverse_lazy('categories_list')


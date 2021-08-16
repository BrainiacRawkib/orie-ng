from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView, CreateView, UpdateView
from django.utils.text import slugify

from accounts.models import User
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .models import Product, Category
from .forms import Review, ReviewForm, ProductAddForm
from .filters import ProductFilter
from .recommender import Recommender


class RobotsTxt(TemplateView):
    def get(self, request, *args, **kwargs):
        lines = [
            "User-Agent: *",
            "Disallow: /orieng-admin/",
            "Disallow: /accounts/",
        ]
        return HttpResponse('\n'.join(lines), content_type='text/plain')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        mvp_merchants = User.objects.filter(is_merchant=True, is_mvp=True)
        context = {
            'title': 'Welcome to Orieng Store ☺',
            'mvp_merchants': mvp_merchants
        }
        return render(self.request, 'stores/home.html', context)


class SearchView(View):

    def get(self, request, *args, **kwargs):
        results = None
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            search_similarity = TrigramSimilarity('name', keyword)
            results = Product.objects.annotate(
                similarity=search_similarity,).filter(similarity__gt=0.1).order_by('-similarity')
        context = {
            'title': f"{self.request.GET['keyword']} results",
            'values': self.request.GET,
            'results': results,
        }
        return render(self.request, 'stores/search.html', context)


class ProductListingsView(ListView):
    model = Product
    template_name = 'stores/products/product_listings.html'
    queryset = Product.stocked.order_by('-date_added')
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        category = None
        categories = Category.objects.order_by('name')
        products = self.get_queryset()
        if self.kwargs.get('slug'):
            category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
            products = products.filter(category=category)
        context = {
            'title': 'Store',
            'categories': categories,
            'category': category,
        }
        return super(ProductListingsView, self).get_context_data(object_list=products, **context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'stores/products/product_detail.html'
    r = Recommender()

    def get_cart_product_form(self):
        return CartAddProductForm()

    def get_review_form(self, data=None):
        return ReviewForm(data=data)

    def get(self, request, *args, **kwargs):
        cart = Cart(self.request)
        cart_items = [item['product'] for item in cart]
        self.r.products_bought(cart_items)
        return self.render_to_response({
            'product': self.get_object(),
            'title': self.get_object().name,
            'cart_product_form': self.get_cart_product_form(),
            'review_form': self.get_review_form(data=None),
            'recommended_products': self.r.suggest_products_for([self.get_object()], 6),
        })

    def post(self, request, *args, **kwargs):
        review_form = self.get_review_form(data=self.request.POST)

        if review_form.is_valid():
            cd = review_form.cleaned_data
            if request.user.is_authenticated:
                if Review.objects.filter(product=self.get_object(), author=self.request.user).exists():
                    messages.error(self.request, f'You have reviewed this product before')
                    return redirect('stores:product-detail', self.get_object().slug)
                Review.objects.create(
                    product=self.get_object(),
                    author=request.user,
                    ratings=cd['ratings'],
                    comment=cd['comment'],
                )
                # return redirect('product/' + self.get_product_details().slug + '/')
                return redirect('stores:product-detail', self.get_object().slug)
        return self.render_to_response({
            'product': self.get_object(),
            'title': self.get_object().name,
            'cart_product_form': self.get_cart_product_form(),
            'review_form': review_form
        })


class ProductCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductAddForm
    permission_denied_message = 'You are not allowed to add a product.'
    template_name = 'stores/products/product_create.html'
    extra_context = {'title': 'Add Product'}
    success_message = 'Product Added!'

    def form_valid(self, form):
        form.instance.merchant = self.request.user if self.request.user.is_merchant else None
        form.instance.slug = slugify(form.instance.name)
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductAddForm
    template_name = 'stores/products/product_update.html'
    success_message = 'Product Updated!'

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context.update({
            'title': f'Update {self.get_object().name}'
        })
        return context

    def form_valid(self, form):
        form.instance.merchant = self.request.user if self.request.user.is_merchant else 'Anonymous'
        return super(ProductUpdateView, self).form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user.is_merchant:
            if self.request.user == product.merchant:
                return True
            return False
        return False


class MerchantStoreView(ListView):
    model = Product
    template_name = 'stores/merchant_store.html'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user.is_merchant:
            return Product.objects.filter(merchant=user)
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super(MerchantStoreView, self).get_context_data(object_list=self.get_queryset(), **kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context_data.update({
            'title': f'{user.username} Store',
            'user': user,
        })
        return context_data

from django.urls import path
from .views import *

app_name = 'stores'

urlpatterns = [
    # stores urls
    path('search/', SearchView.as_view(), name='search'),
    path('product-listings/', ProductListingsView.as_view(), name='product-listings'),
    path('product-listings/<slug:slug>/', ProductListingsView.as_view(), name='product-listings-by-category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-add/', ProductCreateView.as_view(), name='product-add'),
    path('product-update/<slug:slug>/', ProductUpdateView.as_view(), name='product-update'),
    path('<str:username>-store/', MerchantStoreView.as_view(), name='merchant-store'),
    path('', HomeView.as_view(), name='home'),
]

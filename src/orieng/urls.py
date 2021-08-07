from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from stores.sitemaps import ProductSitemap
from stores.views import RobotsTxt


sitemaps = {
    'products': ProductSitemap
}

urlpatterns = [
    path('jet/', include('jet.urls', namespace='jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('orieng-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('help/', include('contacts.urls', namespace='contacts')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', RobotsTxt.as_view()),
    path('', include('stores.urls', namespace='stores')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

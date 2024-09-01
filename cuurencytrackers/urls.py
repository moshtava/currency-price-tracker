from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CryptocurrencyListView, CryptocurrencyDetailByNameView, HistoricalPriceListView

urlpatterns = [
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swaggger-ui'),
]
urlpatterns += [
path('cryptocurrencies/', CryptocurrencyListView.as_view(), name='cryptocurrency-list'),
path('cryptocurrencies/name/<str:name>/', CryptocurrencyDetailByNameView.as_view(), name='cryptocurrency-detail-by-name'),
path('cryptocurrencies/<str:name>/historical-prices/', HistoricalPriceListView.as_view(), name='historical-price-list'),
]
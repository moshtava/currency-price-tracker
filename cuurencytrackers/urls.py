from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import DailyReturnView, GenerateDataView, InsertDataView, RSIView
from .views import CryptocurrencyListView, CryptocurrencyDetailByNameView, HistoricalPriceListView, HistoricalPriceRangeView, DailyReturnView

urlpatterns = [
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swaggger-ui'),
]
urlpatterns += [
path('cryptocurrencies/', CryptocurrencyListView.as_view(), name='cryptocurrency-list'),
path('cryptocurrencies/name/<str:name>/', CryptocurrencyDetailByNameView.as_view(), name='cryptocurrency-detail-by-name'),
path('cryptocurrencies/<str:name>/historical-prices/', HistoricalPriceListView.as_view(), name='historical-price-list'),
path('historical-prices/', HistoricalPriceRangeView.as_view(), name='historical-price-range'),
path('daily-returns/', DailyReturnView.as_view(), name='daily-returns'),
path('rsi/', RSIView.as_view(), name='rsi'),
]
urlpatterns += [
path('generate_data/', GenerateDataView.as_view(), name='generate_data'),
path('insert_data/', InsertDataView.as_view(), name='insert_data'),
]
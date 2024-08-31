from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CryptocurrencyListView

urlpatterns = [
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swaggger-ui'),
]
urlpatterns += [
path('cryptocurrencies/', CryptocurrencyListView.as_view(), name='cryptocurrency-list'),
]
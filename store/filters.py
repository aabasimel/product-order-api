from attrs import fields
import django_filters
from store.models import Product, Order
import django_filters
from rest_framework import filters
class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  

    class Meta:
        model=Product
        fields={'name': ['iexact', 'icontains'],
                'price': ['exact', 'lt', 'gt','range']
                }

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name = 'created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt','exact', 'range']
        }

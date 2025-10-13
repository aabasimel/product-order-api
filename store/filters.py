import django_filters
from store.models import Product
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

import django_filters
from store.models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  

    class Meta:
        model=Product
        fields={'name': ['iexact', 'icontains'],
                'price': ['exact', 'lt', 'gt','range']
                }

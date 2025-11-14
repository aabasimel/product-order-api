from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from store.models import Product
from django.core.cache import cache
from store.serializers import ProductSerializer

@receiver([post_save,post_delete],sender=Product)
def invalidate_product_cache(sender,instance,**kwargs):
    print("Invalidating cache for product list")  

    cache.delete_pattern('*product_list*')
    
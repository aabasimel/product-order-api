
from django.core.cache import cache
from .models import Product
from .serializers import ProductSerializer

def get_all_products():
    cached_products=cache.get("product_list")
    if cached_products is not None:
        print("Returnning cached products")
        return cached_products
    print("Fetching products from DB")

    products=Product.objects.all()

    serialized_product= ProductSerializer(products,many=True).data
    cache.set('product_list',serialized_product,timeout=60*15)
    return {
        "status": "success",
        "status_code": 200,
        "message": "Properties fetched successfully",
        "data": serialized_product
    }
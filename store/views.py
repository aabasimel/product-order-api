from django.http import JsonResponse
from store.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from store.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ProductListAPIView(generics.ListAPIView):
    queryset=Product.objects.all()
    #used to retrieve products where the stock value is not equal to zero
   # queryset=Product.filter(stock__get=0)
   #used to retrieve products where the stock value is equal to zero
    # queryset=Product.exclude(stock__get=0)

    serializer_class=ProductSerializer

# class productCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class=ProductSerializer

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request,*args, **kwargs)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


# @api_view(['GET'])
# def product_list(request):
#     products=Product.objects.all()
#     serializer=ProductSerializer(products, many=True)
#     return Response(serializer.data,status=200)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'



# @api_view(['GET'])
# def product_detail(request,pk):
#     product = get_object_or_404(Product,pk=pk)
#     serializer=ProductSerializer(product)
#     return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView):
#     #queryset=Order.objects.all()
#     queryset=Order.objects.prefetch_related('items__product')

#     serializer_class=OrderSerializer
class UserOrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product')
    serializer_class=OrderSerializer
    permission_classes = [IsAuthenticated]


    def  get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
        
        #return user.accounts.all()
    

# @api_view(['GET'])
# def order_list(request):
#     orders=Order.objects.all()
#     serializer=OrderSerializer(orders, many=True)
#     return Response(serializer.data,status=200)


class ProductInfoAPIView(APIView):
    def product_info(request):
        products=Product.objects.all()
        serializer=ProductInfoSerializer({
        'products':products,
        'count': len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    }
    )
        return Response(serializer.data)



# @api_view(['GET'])
# def product_info(request):
#     products=Product.objects.all()
#     serializer=ProductInfoSerializer({
#         'products':products,
#         'count': len(products),
#         'max_price':products.aggregate(max_price=Max('price'))['max_price']
#     }
#     )
#     return Response(serializer.data)



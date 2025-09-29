from django.http import JsonResponse
from store.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer
from store.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404



@api_view(['GET'])
def product_list(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products, many=True)
    return Response(serializer.data,status=200)


@api_view(['GET'])
def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    serializer=ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders=Order.objects.all()
    serializer=OrderSerializer(orders, many=True)
    return Response(serializer.data,status=200)

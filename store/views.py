from django.http import JsonResponse
from store.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer, OrderCreateSerializer, LoginSerializer,RegisterSerializer
from .models import Product,Order,OrderItem,User
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser, 
    AllowAny)
from rest_framework.views import APIView
from store.filters import ProductFilter,InStockFilterBackend, OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, viewsets

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from store.tasks import send_order_confirmation_email,send_verification_email

from .utils import generate_email_token
from django.conf import settings
import jwt
from rest_framework.generics import GenericAPIView
from urllib.parse import unquote
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken

# class ProductListAPIView(generics.ListAPIView):
#     queryset=Product.objects.all().order_by('id')
#     #used to retrieve products where the stock value is not equal to zero
#    # queryset=Product.filter(stock__get=0)
#    #used to retrieve products where the stock value is equal to zero
#     # queryset=Product.exclude(stock__get=0)

#     serializer_class=ProductSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  
#     #filterset_fields = ['name','price'] 
#     filterset_class=ProductFilter

    #search_fields = ['name'] 

# class productCreateAPIView(generics.CreateAPIView):
#     model =  Product
#     serializer_class=ProductSerializer

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request,*args, **kwargs)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.order_by('pk')
    serializer_class=ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend] 
    #filterset_fields = ['name','price'] 
    filterset_class=ProductFilter
    search_fields = ['=name', 'description'] 
    ordering_fields= ['name','price', 'stock']
    #pagination_class = PageNumberPagination
    #pagination_class=LimitOffsetPagination
    # pagination_class.page_size=2
    # pagination_class.page_query_param= 'pagenum'
    # pagination_class.page_size_query_param= 'size'
    # pagination_class.max_page_size=6
    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)

    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method =='POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


    def get_queryset(self):
        import time
        time.sleep(10)
        return super().get_queryset()

# @api_view(['GET'])
# def product_list(request):
#     products=Product.objects.all()
#     serializer=ProductSerializer(products, many=True)
#     return Response(serializer.data,status=200)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method in ['PUT', 'PATCH','DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
#     lookup_url_kwarg='product_id'



# @api_view(['GET'])
# def product_detail(request,pk):
#     product = get_object_or_404(Product,pk=pk)
#     serializer=ProductSerializer(product)
#     return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView):
#     #queryset=Order.objects.all()
#     queryset=Order.objects.prefetch_related('items__product')

#     serializer_class=OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def  perform_create(self,serializer):
        order=serializer.save(user=self.request.user)
        send_order_confirmation_email.delay(order.order_id,self.request.user.email)
    def get_serializer_class(self):
        # can also check if POST: if self.request.method == 'POST'
        if self.action == 'create' or 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        
        qs=super().get_queryset()
        if not self.request.user.is_staff:
            qs=qs.filter(user=self.request.user)
        return qs
    

    # @action(detail=False, methods=['get'], url_path='user-orders')
    # def user_orders(self, request):
    #     orders=self.get_queryset().filter(user=request.user)
    #     serializer=self.get_serializer(orders, many=True)
    #     return Response(serializer.data)

#     queryset=Order.objects.prefetch_related('items__product')
#     serializer_class=OrderSerializer
#     permission_classes = [IsAuthenticated]


#     def  get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
        
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



class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.filter(email=email).first()

        if user:
            if user.is_active:
                # Email already verified → cannot register again
                return Response({"error": "Email already registered"}, status=400)
            else:
                # User exists but not verified → resend verification email
                token = generate_email_token(user)
                verification_link = f"http://localhost:8080/verify-email?token={token}"
                send_verification_email.delay(email, verification_link)
                return Response({"message": "Verification email resent"}, status=200)
        else:
            # New user → create and send verification email
            user = User.objects.create_user(email=email, password=password)
            user.is_active = False
            user.save()

            token = generate_email_token(user)
            verification_link = f"http://localhost:8080/verify-email?token={token}"
            send_verification_email.delay(email, verification_link)

            return Response({"message": "Verification email sent"}, status=201)
     



class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token', '').strip()
        if not token:
            return Response({"error": "Token is required"}, status=400)

        # decode URL-encoded token
        token = unquote(token)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')

            user = User.objects.get(id=user_id)

            if user.is_active:
                return Response({"message": "Account already verified"}, status=200)

            # Activate the user
            user.is_active = True
            user.save()

            return Response({"message": "Email verified successfully"}, status=200)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=400)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.is_active:
            return Response({"error": "Email not verified"}, status=403)

        # ✔ Generate REAL SimpleJWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "refresh": str(refresh),
            "access": str(access),
        }, status=200)
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [

    path("products/", views.ProductListCreateAPIView.as_view()),
    # path('products/',views.product_list),
    #path('products/',views.ProductListAPIView.as_view()),
    # path('products/info',views.product_info),
    # path('products/<int:pk>/',views.product_detail),
    path('products/<int:product_id>/',views.ProductDetailAPIView.as_view()),
    # path('orders/',views.order_list)
    #path("orders/",views.OrderListAPIView.as_view()),
    #path("user-orders/",views.UserOrderListAPIView.as_view(), name="user-orders"),
    #path('products/create/',views.productCreateAPIView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('verify-email/',views.VerifyEmailView.as_view()),
    path('login/',views.LoginView.as_view()),
   
  




]
router= DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls
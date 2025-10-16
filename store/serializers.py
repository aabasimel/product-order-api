from rest_framework import serializers
from .models import Product,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            
            'name',
            'description',
            'price',
            'stock',

        )
    def validate_price(self, value):
        if value<=0:
            raise serializers.ValidationError(
                "price must be greater than 0"
            )
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name')
    product_price=serializers.DecimalField(max_digits=10,decimal_places=2,source='product.price')

    class Meta:
        model=OrderItem
        fields=(
            
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',

        )

class OrderCreateSerializer(serializers.ModelSerializer):

    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model=OrderItem
            fields = ('product', 'quantity')
    items=OrderItemCreateSerializer(many=True)
    
    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')
        instance = super().update(instance, validated_data)
        if orderitem_data is not None:
            # clear existing items (optional, depending on requirement)
            instance.items.all().delete()

            for item in orderitem_data:
                OrderItem.objects.create(order=instance, **item)
        return instance










    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in orderitem_data:
            OrderItem.objects.create(order=order, **item)
        return order


    class Meta:
        model = Order
        fields = (
            'user',
            'status',
            'items',
            
        )
    
    
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items=OrderItemSerializer(many=True, read_only=True)
    total_price=serializers.SerializerMethodField()

    def get_total_price(self,obj):
        order_items=obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model=Order
        fields=(
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',
        )

class ProductInfoSerializer(serializers.Serializer):
    # get all products, count of products, max price
    products = ProductSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.FloatField()
    

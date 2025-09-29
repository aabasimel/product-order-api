import os
import django
import random
from decimal import Decimal
from faker import Faker

import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_order_api.settings')

django.setup()


from store.models import User, Product, Order, OrderItem

fake = Faker()

# Clear existing data (optional)
User.objects.all().delete()
Product.objects.all().delete()
Order.objects.all().delete()
OrderItem.objects.all().delete()

# Create random users
users = []
for _ in range(5):
    user = User.objects.create_user(
        username=fake.user_name(),
        password='password123'
    )
    users.append(user)

# Create random products
products = []
for _ in range(10):
    product = Product.objects.create(
        name=fake.word().title(),
        description=fake.sentence(),
        price=Decimal(random.randint(100, 10000)) / 100,  # Random price 1.00–100.00
        stock=random.randint(0, 50)
    )
    products.append(product)

# Create random orders
for _ in range(8):
    user = random.choice(users)
    order = Order.objects.create(user=user)
    
    # Add 1-5 random products to order
    for _ in range(random.randint(1, 5)):
        product = random.choice(products)
        quantity = random.randint(1, 3)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

print("✅ Random data seeded successfully!")

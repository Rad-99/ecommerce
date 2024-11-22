import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Category_choices = ( 
    ('CE', 'Coffee'),
    ('FJ', 'Fruit Juices'),
    ('SD', 'Soft Drinks'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)  
    selling_price = models.FloatField() 
    description = models.TextField()
    composition = models.TextField(default='')    
    prodapp = models.TextField(default='') 
    category = models.CharField(choices=Category_choices, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title 


class Customer(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # Add this line
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, blank=True, null=True)

class Cart(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

    def __str__(self):  # Optionally add a string representation for better readability
        return f"{self.product.title} in cart of {self.user.username}"
    
class Order(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    # customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit at time of order

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"





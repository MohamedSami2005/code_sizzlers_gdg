from django.db import models
from django.contrib.auth.models import User
from uzhavan_hub.models import Produce

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Tamil Nadu')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.city})"

class Cart(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.consumer}"

    def total_amount(self):
        return sum(item.total_price() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.FloatField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}kg of {self.produce.name}"

    def total_price(self):
        return self.quantity * self.produce.price_per_kg

class Order(models.Model):
    ORDER_STATUS = (
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('X', 'Cancelled'),
    )

    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()
    contact_number = models.CharField(max_length=15)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='P')
    payment_method = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.consumer}"
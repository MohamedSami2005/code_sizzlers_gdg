from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

PRODUCE_GRADES = (
    ('A', 'Grade A - Premium Quality'),
    ('B', 'Grade B - Good Quality'),
    ('C', 'Grade C - Standard Quality'),
)

PRODUCE_CATEGORIES = (
    ('FR', 'Fruits'),
    ('VE', 'Vegetables'),
    ('GR', 'Grains'),
    ('DA', 'Dairy'),
    ('OT', 'Others'),
)

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Tamil Nadu')
    aadhaar_number = models.CharField(max_length=12, unique=True)
    bank_account = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)
    verified = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.village})"

class UzhavanHub(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    operational_hours = models.CharField(max_length=100, default='6 AM - 6 PM')

    def __str__(self):
        return self.name

class Produce(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    hub = models.ForeignKey(UzhavanHub, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=PRODUCE_CATEGORIES)
    quantity = models.FloatField(validators=[MinValueValidator(0.1)])
    grade = models.CharField(max_length=1, choices=PRODUCE_GRADES)
    price_per_kg = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='produce_images/')
    available = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_grade_display()}) - {self.farmer}"

    def total_price(self):
        return self.quantity * self.price_per_kg
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

# Constants
PRODUCE_GRADES = (
    ('A', _('Grade A - Premium Quality')),
    ('B', _('Grade B - Good Quality')),
    ('C', _('Grade C - Standard Quality')),
)

PRODUCE_CATEGORIES = (
    ('FR', _('Fruits')),
    ('VE', _('Vegetables')),
    ('GR', _('Grains')),
    ('DA', _('Dairy')),
    ('OT', _('Others')),
)

class Farmer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='farmer_profile'
    )
    phone = models.CharField(
        _('Phone Number'),
        max_length=15,
        validators=[RegexValidator(r'^[0-9]{10,15}$')]
    )
    village = models.CharField(_('Village'), max_length=100)
    district = models.CharField(_('District'), max_length=100)
    state = models.CharField(
        _('State'),
        max_length=100,
        default='Tamil Nadu'
    )
    aadhaar_number = models.CharField(
        _('Aadhaar Number'),
        max_length=12,
        null=True,
        blank=True,
        unique=True,
        validators=[RegexValidator(r'^[0-9]{12}$')]
    )
    bank_account = models.CharField(
        _('Bank Account Number'),
        max_length=20,
        validators=[RegexValidator(r'^[0-9]{9,18}$')]
    )
    ifsc_code = models.CharField(
        _('IFSC Code'),
        max_length=11,
        validators=[RegexValidator(r'^[A-Z]{4}0[A-Z0-9]{6}$')]
    )
    verified = models.BooleanField(_('Verified'), default=False)
    registration_date = models.DateTimeField(
        _('Registration Date'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('Farmer')
        verbose_name_plural = _('Farmers')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.village})"

class UzhavanHub(models.Model):
    name = models.CharField(_('Hub Name'), max_length=100)
    location = models.CharField(_('Location'), max_length=200)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_hubs'
    )
    contact_number = models.CharField(
        _('Contact Number'),
        max_length=15,
        validators=[RegexValidator(r'^[0-9]{10,15}$')]
    )
    latitude = models.DecimalField(
        _('Latitude'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        _('Longitude'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    operational_hours = models.CharField(
        _('Operational Hours'),
        max_length=100,
        default='6 AM - 6 PM'
    )

    class Meta:
        verbose_name = _('Uzhavan Hub')
        verbose_name_plural = _('Uzhavan Hubs')

    def __str__(self):
        return self.name

class Produce(models.Model):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        related_name='produces'
    )
    hub = models.ForeignKey(
        UzhavanHub,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hub_produces'
    )
    name = models.CharField(_('Produce Name'), max_length=100)
    category = models.CharField(
        _('Category'),
        max_length=2,
        choices=PRODUCE_CATEGORIES
    )
    quantity = models.FloatField(
        _('Quantity (kg)'),
        validators=[MinValueValidator(0.1)]
    )
    grade = models.CharField(
        _('Quality Grade'),
        max_length=1,
        choices=PRODUCE_GRADES
    )
    price_per_kg = models.DecimalField(
        _('Price per kg (₹)'),
        max_digits=6,
        decimal_places=2
    )
    description = models.TextField(_('Description'), blank=True)
    listed_at = models.DateTimeField(_('Listed At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    image = models.ImageField(
        _('Product Image'),
        upload_to='produce_images/'
    )
    available = models.BooleanField(_('Available'), default=True)
    approved = models.BooleanField(_('Approved'), default=False)

    class Meta:
        verbose_name = _('Produce')
        verbose_name_plural = _('Produces')
        ordering = ['-listed_at']

    def __str__(self):
        return f"{self.name} ({self.get_grade_display()}) - {self.farmer}"

    @property
    def total_price(self):
        """Calculate total price for the available quantity"""
        return round(self.quantity * self.price_per_kg, 2)
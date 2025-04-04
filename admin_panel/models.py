from django.db import models
from uzhavan_hub.models import Farmer, UzhavanHub, Produce
from consumer_app.models import Consumer, Order

class Dispute(models.Model):
    DISPUTE_TYPES = (
        ('Q', 'Quality Issue'),
        ('D', 'Delivery Issue'),
        ('P', 'Payment Issue'),
        ('O', 'Other'),
    )

    STATUS_CHOICES = (
        ('O', 'Open'),
        ('I', 'In Progress'),
        ('R', 'Resolved'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    raised_by = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    dispute_type = models.CharField(max_length=1, choices=DISPUTE_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='O')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution = models.TextField(blank=True)

    def __str__(self):
        return f"Dispute #{self.id} - {self.get_dispute_type_display()}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('F', 'Farmer Verification'),
        ('O', 'New Order'),
        ('D', 'Dispute'),
        ('S', 'System Update'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.recipient}"
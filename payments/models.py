import uuid
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    PRODUCT_TYPES = [
        ("one_time", "One-Time Purchase"),
        ("subscription_monthly", "Monthly Subscription"),
        ("subscription_annual", "Annual Subscription"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300, blank=True)
    price_paise = models.PositiveIntegerField(
        help_text="Price in paise.  ₹99 → 9900,  ₹299 → 29900"
    )
    product_type = models.CharField(max_length=30, choices=PRODUCT_TYPES, default="one_time")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price_paise"]

    def __str__(self):
        return f"{self.name} (₹{self.price_paise // 100})"

    @property
    def price_rupees(self):
        return self.price_paise // 100


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orders")

    # Razorpay identifiers
    razorpay_order_id = models.CharField(max_length=200, unique=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True)
    razorpay_signature = models.CharField(max_length=500, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    amount_paise = models.PositiveIntegerField()

    # Anonymous / pre-login flow support
    email = models.EmailField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)

    # Delivery tracking
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} — {self.status} — ₹{self.amount_paise // 100}"

    @property
    def amount_rupees(self):
        return self.amount_paise // 100


class Subscription(models.Model):
    TIER_CHOICES = [("pro", "Pro"), ("team", "Team")]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    started_at = models.DateTimeField()
    expires_at = models.DateTimeField()

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.email} — {self.tier} — {self.status}"

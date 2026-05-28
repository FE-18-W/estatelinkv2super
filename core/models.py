from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Declined', 'Declined'),
]


class Estate(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profiles')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


class WaterVendor(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='watervendor')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='water_vendors')
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GasVendor(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='gasvendor')
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='gas_vendors')
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ShopOwner(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='shopowner')
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='shop_owners')
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WaterOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_orders')
    vendor = models.ForeignKey(WaterVendor, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    driver_name = models.CharField(max_length=100, blank=True)
    eta_minutes = models.IntegerField(null=True, blank=True)
    litres = models.IntegerField(null=True, blank=True, help_text="Litres of water needed")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price willing to pay (KSh)")
    vendor_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class GasOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gas_orders')
    vendor = models.ForeignKey(GasVendor, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    kgs = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    block_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    vendor_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gas order #{self.id} by {self.customer.username}"


class ShopOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_orders')
    owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name='orders')
    item_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    owner_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shop order #{self.id} - {self.item_name}"


class GarbageSchedule(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='garbage_schedules')
    collection_day = models.CharField(max_length=20)
    time = models.TimeField()


class ServiceCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='service_provider')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='providers')
    verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    available = models.BooleanField(default=True)


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bookings')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class SecurityAlert(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='security_alerts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_alerts')
    created_at = models.DateTimeField(auto_now_add=True)


class LostItem(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='lost_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_items')
    is_found = models.BooleanField(default=False)


class Gig(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='gigs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_gigs')


class MarketItem(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='market_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='market_items')
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='market/', blank=True, null=True)


class BillReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bill_reminders')
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='bill_reminders', null=True, blank=True)
    title = models.CharField(max_length=100)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default='active', choices=[
        ('active', 'Active'),
        ('pending_confirmation', 'Pending Confirmation'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_bills')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_bills')
    paid_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FundiRequest(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='fundi_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fundi_requests')
    requester_name = models.CharField(max_length=100)
    requester_phone = models.CharField(max_length=15, blank=True)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL, null=True, blank=True)
    fundi_type = models.CharField(max_length=100)
    time_needed = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    admin_response = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fundi_type} - {self.requester_name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, default='general')
    related_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # NEW FIELD: For tracking broadcast deletions
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class EstateAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estate_admin')
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='estate_admins')
    is_subscribed = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_admins')
    approved_at = models.DateTimeField(null=True, blank=True)
    can_manage_users = models.BooleanField(default=False)
    can_manage_requests = models.BooleanField(default=False)
    can_manage_alerts = models.BooleanField(default=False)
    can_manage_services = models.BooleanField(default=False)
    can_manage_bills = models.BooleanField(default=False)
    can_manage_tabs = models.BooleanField(default=False)
    can_view_analytics = models.BooleanField(default=False)
    can_broadcast = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Admin of {self.estate.name}"


class VendorDeletionRequest(models.Model):
    VENDOR_TYPE_CHOICES = [
        ('gas', 'Gas Vendor'),
        ('shop', 'Shop Owner'),
        ('water', 'Water Vendor'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    vendor_type = models.CharField(max_length=10, choices=VENDOR_TYPE_CHOICES)
    vendor_id = models.PositiveIntegerField()
    vendor_name = models.CharField(max_length=100)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='vendor_deletions')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_deletion_requests')
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_vendor_deletions')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor_name} ({self.get_vendor_type_display()}) - {self.status}"


class CustomTab(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='custom_tabs')
    name = models.CharField(max_length=100)
    icon_svg = models.TextField(blank=True)
    url = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default="#00f2fe")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_tabs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.estate.name})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            User.objects.filter(pk=instance.pk).update(is_active=False)
        default_estate = Estate.objects.first()
        UserProfile.objects.create(user=instance, estate=default_estate)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
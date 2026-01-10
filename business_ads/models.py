from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    """Business customers/clients"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('lead', 'Lead'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.email})"

class Promotion(models.Model):
    """Marketing promotions/campaigns"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promotions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    TYPE_CHOICES = [
        ('discount', 'Discount'),
        ('social', 'Social Media'),
        ('email', 'Email Campaign'),
        ('event', 'Event'),
        ('other', 'Other'),
    ]
    promotion_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='discount')
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Performance metrics
    reach = models.IntegerField(default=0)  # Number of people reached
    conversions = models.IntegerField(default=0)  # Number of conversions
    revenue_generated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date
    
    @property
    def roi(self):
        """Return Return on Investment percentage"""
        if self.budget > 0:
            return ((self.revenue_generated - self.budget) / self.budget) * 100
        return 0

class Revenue(models.Model):
    """Monthly revenue tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revenues')
    month = models.DateField()  # First day of month
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=100, default='sales')
    
    class Meta:
        ordering = ['-month']
        unique_together = ['user', 'month', 'source']
    
    def __str__(self):
        return f"{self.month.strftime('%B %Y')}: ${self.amount}"

class Activity(models.Model):
    """Recent activities/log"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='info-circle')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.activity_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class BusinessLocation(models.Model):
    """Business locations for map"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    TYPE_CHOICES = [
        ('headquarters', 'Headquarters'),
        ('branch', 'Branch'),
        ('store', 'Store'),
        ('warehouse', 'Warehouse'),
        ('other', 'Other'),
    ]
    location_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='store')
    
    customers_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

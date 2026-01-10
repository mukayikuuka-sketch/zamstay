from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    preferences = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Promotion(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_type = models.CharField(max_length=50, choices=[
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('buy_one_get_one', 'Buy One Get One')
    ])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class MapView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text='View duration in seconds')
    
    class Meta:
        unique_together = ['user', 'business', 'viewed_at']

class Analytics(models.Model):
    date = models.DateField(unique=True)
    total_users = models.IntegerField()
    active_users = models.IntegerField()
    map_views = models.IntegerField()
    promotion_views = models.IntegerField()
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f'Analytics for {self.date}'

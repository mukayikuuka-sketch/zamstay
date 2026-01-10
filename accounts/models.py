from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('owner', 'Property Owner'),
        ('guest', 'Guest'),
        ('admin', 'Administrator'),
    )
    
    role = models.CharField(max_length=10, choices=USER_ROLES, default='guest')
    phone_number = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # Owner-specific fields
    company_name = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Guest-specific fields
    nationality = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['-date_joined']

# api_apps/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class CustomerSegment(models.Model):
    """
    Model for storing customer segments
    """
    
    # Segment Types
    SEGMENT_TYPE_CHOICES = [
        ('behavioral', 'Behavioral'),
        ('demographic', 'Demographic'),
        ('activity', 'Activity'),
        ('risk', 'Risk'),
        ('value', 'Value'),
        ('custom', 'Custom'),
    ]
    
    # Basic Information
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    segment_type = models.CharField(max_length=50, choices=SEGMENT_TYPE_CHOICES, default='custom')
    
    # Criteria (stored as JSON)
    criteria = models.JSONField(default=dict)
    
    # Auto refresh settings
    auto_refresh = models.BooleanField(default=False)
    refresh_interval = models.CharField(max_length=20, default='daily', choices=[
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ])
    
    # Statistics
    customer_count = models.IntegerField(default=0)
    last_refresh = models.DateTimeField(default=timezone.now)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False)  # System-defined vs user-defined
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'customer_segments'
        verbose_name = 'Customer Segment'
        verbose_name_plural = 'Customer Segments'
        ordering = ['-last_refresh', '-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.customer_count})"
    
    def save(self, *args, **kwargs):
        # Generate ID if not provided
        if not self.id:
            prefix = 'seg_' if not self.is_system else 'sys_seg_'
            self.id = f"{prefix}{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        # Ensure criteria is a dict
        if isinstance(self.criteria, str):
            try:
                self.criteria = json.loads(self.criteria)
            except:
                self.criteria = {}
        
        super().save(*args, **kwargs)
    
    def formatted_customer_count(self):
        """Format customer count with commas"""
        return f"{self.customer_count:,}"
    
    def refresh_count(self):
        """Refresh customer count based on criteria"""
        # This would run actual queries based on criteria
        # For now, return mock data
        from .mock_data import MockDataGenerator
        return MockDataGenerator.get_segment_customer_count(self.id)
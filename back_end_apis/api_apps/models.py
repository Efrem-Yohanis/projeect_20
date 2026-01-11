# api_apps/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import json
import uuid

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


class RewardAccount(models.Model):
    """
    Financial container (wallet) used to fund incentive campaigns.
    """
    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        FROZEN = 'frozen', 'Frozen (No Outgoing)'

    # Identification
    account_id = models.CharField(max_length=100, unique=True)
    account_name = models.CharField(max_length=255)

    # Financials
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='ETB')

    # State
    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE
    )

    # Relationships
    # Using ManyToMany allows a 'General Marketing Fund' to be shared across many campaigns
    # assigned_campaigns = models.ManyToManyField(
    #     'Campaign',
    #     related_name='reward_accounts',
    #     blank=True,
    #     help_text="Campaigns authorized to draw rewards from this account."
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['account_name']
        verbose_name = "Reward Account"
        verbose_name_plural = "Reward Accounts"

    def __str__(self):
        return f"{self.account_name} - {self.balance} {self.currency}"

    def clean(self):
        """Prevent negative balances at the model level."""
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative.")

    # Helper methods for business logic
    @property
    def is_available(self):
        return self.status == self.AccountStatus.ACTIVE


class Campaign(models.Model):
    class CampaignType(models.TextChoices):
        INCENTIVE = 'incentive', 'Incentive'
        INFORMATIONAL = 'informational', 'Informational'
        WIN_BACK = 'win_back', 'Win-back'
        INFO = 'info', 'Info'

    class CampaignStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING_APPROVAL = 'pending_approval', 'Pending Approval'
        SCHEDULED = 'scheduled', 'Scheduled'
        RUNNING = 'running', 'Running'
        PAUSED = 'paused', 'Paused'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        CANCELLED = 'cancelled', 'Cancelled'

    class ScheduleType(models.TextChoices):
        IMMEDIATE = 'immediate', 'Immediate'
        SCHEDULED = 'scheduled', 'Scheduled'

    class RewardType(models.TextChoices):
        CASHBACK = 'cashback', 'Cashback'
        BONUS = 'bonus', 'Bonus'
        OTHER = 'other', 'Other'

    class FrequencyCap(models.TextChoices):
        DAILY = 'daily', 'Daily'
        WEEKLY = 'weekly', 'Weekly'
        MONTHLY = 'monthly', 'Monthly'
        UNLIMITED = 'unlimited', 'Unlimited'
        ONCE_PER_DAY = 'once_per_day', 'Once Per Day'

    # Basic Info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=20, choices=CampaignType.choices)
    objective = models.TextField()
    description = models.TextField()
    channels = models.JSONField(default=list, help_text="List of channels like ['SMS', 'Push', 'Email']")
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='campaigns')

    # Status & Flow
    status = models.CharField(max_length=25, choices=CampaignStatus.choices, default=CampaignStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_on = models.DateTimeField(null=True, blank=True)

    # Rewards - Now linked to RewardAccount model
    reward_type = models.CharField(max_length=20, choices=RewardType.choices, null=True, blank=True)
    reward_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reward_account = models.ForeignKey(RewardAccount, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Scheduling
    schedule_type = models.CharField(max_length=20, choices=ScheduleType.choices, default=ScheduleType.IMMEDIATE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    frequency_cap = models.CharField(max_length=20, choices=FrequencyCap.choices, default=FrequencyCap.UNLIMITED)

    # Audience
    selected_segment_ids = models.JSONField(default=list, help_text="List of selected segment UUIDs")
    uploaded_file = models.JSONField(null=True, blank=True, help_text="Uploaded file details for custom targeting")
    total_targeted_customers = models.PositiveIntegerField(default=0, help_text="Total number of targeted customers")

    # Communication
    messages = models.JSONField(default=dict, help_text="Channel-specific messages")
    email_config = models.JSONField(null=True, blank=True, help_text="Email configuration")
    channel_settings = models.JSONField(default=dict, help_text="Channel-specific settings")

    # Rewards
    reward_caps = models.JSONField(default=dict, help_text="Reward caps configuration")

    # Approval
    current_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_campaigns')
    approval_level = models.PositiveIntegerField(default=1)
    segment = models.ForeignKey(CustomerSegment, on_delete=models.CASCADE)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")

    def __str__(self):
        return f"{self.campaign_id or 'Draft'} - {self.name}"


class ApprovalTrail(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='approval_trails')
    approver = models.ForeignKey(User, on_delete=models.PROTECT)
    decision = models.CharField(max_length=15, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.campaign.name} - {self.approver.username} - {self.decision}"


class ReportConfiguration(models.Model):
    """
    Model for storing report configurations for automated reporting
    """
    
    class SourceType(models.TextChoices):
        CAMPAIGN = 'campaign', 'Campaign'
        CUSTOM = 'custom', 'Custom'
    
    class CustomMode(models.TextChoices):
        SQL = 'sql', 'SQL Query'
        FILTER = 'filter', 'Filter Builder'
    
    class ExportFormat(models.TextChoices):
        PDF = 'pdf', 'PDF'
        EXCEL = 'excel', 'Excel'
        CSV = 'csv', 'CSV'
    
    class Frequency(models.TextChoices):
        DAILY = 'daily', 'Daily'
        WEEKLY = 'weekly', 'Weekly'
        MONTHLY = 'monthly', 'Monthly'
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.CUSTOM)
    
    # Configuration
    configuration = models.JSONField(default=dict, help_text="Report configuration details")
    
    # Export settings
    export_format = models.CharField(max_length=10, choices=ExportFormat.choices, default=ExportFormat.PDF)
    
    # Scheduling
    scheduling_enabled = models.BooleanField(default=False)
    frequency = models.CharField(max_length=10, choices=Frequency.choices, blank=True)
    recipients = models.JSONField(default=list, help_text="List of email recipients")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'report_configurations'
        verbose_name = 'Report Configuration'
        verbose_name_plural = 'Report Configurations'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_configuration_display(self):
        """Return a human-readable configuration summary"""
        if self.source_type == self.SourceType.CAMPAIGN:
            campaign_id = self.configuration.get('campaign_id', 'N/A')
            return f"Campaign Report: {campaign_id}"
        else:
            mode = self.configuration.get('custom_mode', 'filter')
            if mode == 'sql':
                return "Custom SQL Query"
            else:
                filters_count = len(self.configuration.get('filters', []))
                return f"Custom Filter ({filters_count} filters)"
    
    def get_scheduling_display(self):
        """Return scheduling information"""
        if not self.scheduling_enabled:
            return "Not scheduled"
        return f"{self.frequency.title()} to {len(self.recipients)} recipients"



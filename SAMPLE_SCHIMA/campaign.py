
class Campaign(models.Model):
    class CampaignType(models.TextChoices):
        INCENTIVE = 'incentive', 'Incentive'
        INFORMATIONAL = 'informational', 'Informational'
    
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

    # Basic Info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=20, choices=CampaignType.choices)
    objective = models.TextField()
    description = models.TextField()
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
    frequency_cap = models.CharField(max_length=20, choices=FrequencyCap.choices)

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

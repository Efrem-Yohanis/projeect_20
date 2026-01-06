from django.db import models
from django.core.exceptions import ValidationError

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
    assigned_campaigns = models.ManyToManyField(
        'Campaign', 
        related_name='reward_accounts', 
        blank=True,
        help_text="Campaigns authorized to draw rewards from this account."
    )

    # Timestamps
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
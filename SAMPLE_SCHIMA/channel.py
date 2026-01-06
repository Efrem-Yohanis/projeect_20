
class CampaignChannel(models.Model):
    class ChannelType(models.TextChoices):
        SMS = 'sms', 'SMS'
        USSD = 'ussd', 'USSD'
        APP_PUSH = 'app', 'App Push'
        EMAIL = 'email', 'Email'
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='channels')
    channel_type = models.CharField(max_length=10, choices=ChannelType.choices)
    enabled = models.BooleanField(default=False)
    priority = models.PositiveIntegerField(default=1)
    
    # Email specific fields (Alternative: use a JSONField for channel-specific configs)
    email_subject = models.CharField(max_length=255, null=True, blank=True)
    email_body = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.campaign.name} - {self.get_channel_type_display()}"

class ChannelMessage(models.Model):
    class LanguageCode(models.TextChoices):
        ENGLISH = 'en', 'English'
        AMHARIC = 'am', 'Amharic'
        AFAN_OROMO = 'om', 'Afaan Oromo'
        # ... keep others
    
    channel = models.ForeignKey(CampaignChannel, on_delete=models.CASCADE, related_name='messages')
    language_code = models.CharField(max_length=5, choices=LanguageCode.choices)
    content = models.TextField()

    def __str__(self):
        return f"{self.channel} ({self.language_code})"

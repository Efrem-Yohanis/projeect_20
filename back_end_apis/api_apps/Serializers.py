# api_apps/serializers.py
from rest_framework import serializers
from .models import CustomerSegment, RewardAccount, Campaign, ApprovalTrail, ReportConfiguration

class CriteriaSerializer(serializers.Serializer):
    """Serializer for segment criteria"""
    # Define fields based on your criteria structure
    status = serializers.CharField(required=False)
    churn_risk = serializers.CharField(required=False)
    lifetime_value_min = serializers.FloatField(required=False)
    lifetime_value_max = serializers.FloatField(required=False)
    last_active_days_min = serializers.IntegerField(required=False)
    last_active_days_max = serializers.IntegerField(required=False)
    registration_date_from = serializers.DateField(required=False)
    registration_date_to = serializers.DateField(required=False)
    engagement_score_min = serializers.FloatField(required=False)
    engagement_score_max = serializers.FloatField(required=False)
    subscription_active = serializers.BooleanField(required=False)

class CustomerSegmentSerializer(serializers.ModelSerializer):
    formatted_customer_count = serializers.SerializerMethodField()
    criteria = CriteriaSerializer(required=False)
    metadata = serializers.JSONField(required=False)
    action = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomerSegment
        fields = [
            'id', 'name', 'description', 'segment_type',
            'customer_count', 'formatted_customer_count',
            'last_refresh', 'created_at', 'updated_at',
            'auto_refresh', 'refresh_interval',
            'criteria', 'metadata', 'action', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_refresh']
    
    def get_formatted_customer_count(self, obj):
        return f"{obj.customer_count:,}"
    
    def get_action(self, obj):
        return "view"

class SegmentListItemSerializer(serializers.ModelSerializer):
    """Serializer for individual segments in list view - excludes action and metadata"""
    formatted_customer_count = serializers.SerializerMethodField()
    criteria = CriteriaSerializer(required=False)
    
    class Meta:
        model = CustomerSegment
        fields = [
            'id', 'name', 'description', 'segment_type',
            'customer_count', 'formatted_customer_count',
            'last_refresh', 'created_at', 'updated_at',
            'criteria'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_refresh']
    
    def get_formatted_customer_count(self, obj):
        return f"{obj.customer_count:,}"

class SegmentListSerializer(serializers.Serializer):
    """Serializer for segment list response"""
    status = serializers.CharField(default="success")
    segments = SegmentListItemSerializer(many=True)
    pagination = serializers.DictField()
    summary = serializers.DictField()

class CreateSegmentSerializer(serializers.ModelSerializer):
    """Serializer for creating segments with new request format"""
    config = serializers.DictField(required=True)
    filters = serializers.DictField(required=True)
    
    class Meta:
        model = CustomerSegment
        fields = ['name', 'description', 'config', 'filters']
    
    def validate_config(self, value):
        """Validate config JSON"""
        required_keys = ['autoRefresh', 'refreshInterval', 'ruleLogic', 'status']
        if not all(key in value for key in required_keys):
            raise serializers.ValidationError("Config must contain autoRefresh, refreshInterval, ruleLogic, and status")
        return value
    
    def validate_filters(self, value):
        """Validate filters JSON"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Filters must be a JSON object")
        return value
    
    def create(self, validated_data):
        # Extract config and filters
        config = validated_data.pop('config')
        filters = validated_data.pop('filters')
        
        # Map config to model fields
        validated_data['auto_refresh'] = config.get('autoRefresh', False)
        validated_data['refresh_interval'] = config.get('refreshInterval', 'daily')
        
        # Store filters in criteria
        validated_data['criteria'] = filters
        
        # Set segment_type based on filters
        if 'behavioral' in filters:
            validated_data['segment_type'] = 'behavioral'
        elif 'demographic' in filters:
            validated_data['segment_type'] = 'demographic'
        elif 'value' in filters:
            validated_data['segment_type'] = 'value'
        else:
            validated_data['segment_type'] = 'custom'
        
        # Add rule_logic to criteria if present
        if 'ruleLogic' in config:
            validated_data['criteria']['rule_logic'] = config['ruleLogic']
        
        return super().create(validated_data)

class UpdateSegmentSerializer(serializers.ModelSerializer):
    """Serializer for updating segments with new request format"""
    config = serializers.DictField(required=False)
    filters = serializers.DictField(required=False)
    
    class Meta:
        model = CustomerSegment
        fields = ['name', 'description', 'config', 'filters']
    
    def validate_config(self, value):
        """Validate config JSON"""
        if value:
            allowed_keys = ['autoRefresh', 'refreshInterval', 'ruleLogic']
            for key in value:
                if key not in allowed_keys:
                    raise serializers.ValidationError(f"Invalid config key: {key}")
        return value
    
    def validate_filters(self, value):
        """Validate filters JSON"""
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Filters must be a JSON object")
        return value
    
    def update(self, instance, validated_data):
        # Extract config and filters
        config = validated_data.pop('config', None)
        filters = validated_data.pop('filters', None)
        
        # Update config fields
        if config:
            if 'autoRefresh' in config:
                instance.auto_refresh = config['autoRefresh']
            if 'refreshInterval' in config:
                instance.refresh_interval = config['refreshInterval']
            if 'ruleLogic' in config:
                instance.criteria['rule_logic'] = config['ruleLogic']
        
        # Update filters (criteria)
        if filters:
            instance.criteria = filters
        
        # Update segment_type based on filters
        if filters:
            if 'behavioral' in filters:
                instance.segment_type = 'behavioral'
            elif 'demographic' in filters:
                instance.segment_type = 'demographic'
            elif 'value' in filters:
                instance.segment_type = 'value'
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class RewardAccountSerializer(serializers.ModelSerializer):
    """Serializer for RewardAccount model"""
    formatted_balance = serializers.SerializerMethodField()
    is_available = serializers.ReadOnlyField()
    assigned_campaigns_count = serializers.SerializerMethodField()

    class Meta:
        model = RewardAccount
        fields = [
            'id', 'account_id', 'account_name', 'balance', 'formatted_balance',
            'currency', 'status', 'is_available', 'assigned_campaigns_count',
            'assigned_campaigns', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_available', 'assigned_campaigns_count']

    def get_formatted_balance(self, obj):
        """Format balance with currency"""
        return f"{obj.balance:,.2f} {obj.currency}"

    def get_assigned_campaigns_count(self, obj):
        """Get count of assigned campaigns"""
        return obj.assigned_campaigns.count()

    def validate_balance(self, value):
        """Ensure balance is not negative"""
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative.")
        return value

    def validate_account_id(self, value):
        """Ensure account_id is unique"""
        if self.instance and RewardAccount.objects.filter(account_id=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Account ID must be unique.")
        elif not self.instance and RewardAccount.objects.filter(account_id=value).exists():
            raise serializers.ValidationError("Account ID must be unique.")
        return value


class RewardAccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating RewardAccount"""

    class Meta:
        model = RewardAccount
        fields = ['account_id', 'account_name', 'balance', 'currency', 'status']

    def validate_balance(self, value):
        """Ensure balance is not negative"""
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative.")
        return value

    def validate_account_id(self, value):
        """Ensure account_id is unique"""
        if RewardAccount.objects.filter(account_id=value).exists():
            raise serializers.ValidationError("Account ID must be unique.")
        return value


class RewardAccountUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating RewardAccount"""

    class Meta:
        model = RewardAccount
        fields = ['account_name', 'balance', 'currency', 'status']

    def validate_balance(self, value):
        """Ensure balance is not negative"""
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative.")
        return value


class RewardAccountListSerializer(serializers.Serializer):
    """Serializer for reward account list response"""
    status = serializers.CharField(default="success")
    accounts = RewardAccountSerializer(many=True)
    pagination = serializers.DictField()
    summary = serializers.DictField()


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for Campaign model"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    current_approver_name = serializers.CharField(source='current_approver.username', read_only=True, allow_null=True)
    segment_name = serializers.CharField(source='segment.name', read_only=True)
    reward_account_name = serializers.CharField(source='reward_account.account_name', read_only=True, allow_null=True)
    approval_trails_count = serializers.SerializerMethodField()
    formatted_estimated_cost = serializers.SerializerMethodField()
    formatted_reward_value = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id', 'campaign_id', 'name', 'campaign_type', 'objective', 'description', 'channels',
            'owner', 'owner_name', 'status', 'created_at', 'updated_at', 'submitted_on',
            'reward_type', 'reward_value', 'formatted_reward_value', 'reward_account',
            'reward_account_name', 'estimated_cost', 'formatted_estimated_cost',
            'schedule_type', 'start_date', 'end_date', 'frequency_cap',
            'selected_segment_ids', 'uploaded_file', 'total_targeted_customers',
            'messages', 'email_config', 'channel_settings', 'reward_caps',
            'current_approver', 'current_approver_name', 'approval_level', 'segment',
            'segment_name', 'approval_trails_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'approval_trails_count']

    def get_approval_trails_count(self, obj):
        """Get count of approval trails"""
        return obj.approval_trails.count()

    def get_formatted_estimated_cost(self, obj):
        """Format estimated cost"""
        if obj.estimated_cost:
            return f"{obj.estimated_cost:,.2f} ETB"
        return None

    def get_formatted_reward_value(self, obj):
        """Format reward value"""
        if obj.reward_value:
            return f"{obj.reward_value:,.2f}"
        return None

    def validate(self, data):
        """Validate campaign data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("Start date cannot be after end date.")

        return data


class CampaignCreateRequestSerializer(serializers.Serializer):
    """Serializer for campaign creation request with nested structure"""

    basics = serializers.DictField()
    audience = serializers.DictField()
    communication = serializers.DictField()
    rewards = serializers.DictField()
    scheduling = serializers.DictField()
    status = serializers.CharField(default='draft')

    def create(self, validated_data):
        """Create campaign from nested request data"""

        # Extract nested data
        basics = validated_data.get('basics', {})
        audience = validated_data.get('audience', {})
        communication = validated_data.get('communication', {})
        rewards = validated_data.get('rewards', {})
        scheduling = validated_data.get('scheduling', {})
        status = validated_data.get('status', 'draft')

        # Get the current user (you might need to pass this from the view)
        # For now, assume we get it from context or set a default
        owner_id = getattr(self.context.get('request'), 'user', None)
        if owner_id and hasattr(owner_id, 'id'):
            owner_id = owner_id.id
        else:
            # Fallback - get first user or create default
            from django.contrib.auth.models import User
            try:
                owner_id = User.objects.first().id
            except:
                owner_id = None

        # Get segment - use first selected segment or create default
        segment_id = None
        if audience.get('selectedSegmentIds'):
            # For now, assume the first segment ID is valid
            # In real implementation, you'd validate these IDs
            segment_id = audience['selectedSegmentIds'][0] if audience['selectedSegmentIds'] else None

        if not segment_id:
            # Fallback to first segment
            from .models import CustomerSegment
            try:
                segment_id = CustomerSegment.objects.first().id
            except:
                segment_id = None

        # Handle reward account
        reward_account_id = None
        if rewards.get('disbursementAccount') and rewards['disbursementAccount'].get('id'):
            # Try to find reward account by account_name or id
            from .models import RewardAccount
            account_id = rewards['disbursementAccount']['id']
            try:
                reward_account_id = RewardAccount.objects.get(account_name=account_id).id
            except RewardAccount.DoesNotExist:
                try:
                    reward_account_id = RewardAccount.objects.filter(account_id__icontains=account_id).first().id
                except:
                    reward_account_id = None

        # Create campaign with flattened data
        campaign_data = {
            'name': basics.get('name'),
            'campaign_type': basics.get('type'),
            'objective': basics.get('objective'),
            'description': basics.get('description'),
            'owner_id': owner_id,

            'channels': communication.get('enabledChannels', []),
            'selected_segment_ids': audience.get('selectedSegmentIds', []),
            'uploaded_file': audience.get('uploadedFile'),
            'total_targeted_customers': audience.get('totalTargetedCustomers', 0),

            'messages': communication.get('messages', {}),
            'email_config': communication.get('email'),
            'channel_settings': communication.get('settings', {}),

            'reward_type': rewards.get('type'),
            'reward_value': rewards.get('value'),
            'reward_caps': rewards.get('caps', {}),
            'reward_account_id': reward_account_id,

            'schedule_type': scheduling.get('type'),
            'start_date': scheduling.get('startDate'),
            'end_date': scheduling.get('endDate'),
            'frequency_cap': scheduling.get('frequencyCap'),

            'status': status,
            'segment_id': segment_id,
        }

        # Create the campaign
        campaign = Campaign.objects.create(**campaign_data)

        # Generate campaign_id if not provided
        if not campaign.campaign_id:
            campaign.campaign_id = f"CAMP_{campaign.id.hex[:8].upper()}"
            campaign.save()

        return campaign


class CampaignCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Campaign"""

    class Meta:
        model = Campaign
        fields = [
            'name', 'campaign_type', 'objective', 'description', 'channels', 'owner',
            'reward_type', 'reward_value', 'reward_account', 'estimated_cost',
            'schedule_type', 'start_date', 'end_date', 'frequency_cap',
            'segment'
        ]

    def validate(self, data):
        """Validate campaign creation data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("Start date cannot be after end date.")

        return data


class CampaignUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Campaign"""

    class Meta:
        model = Campaign
        fields = [
            'name', 'campaign_type', 'objective', 'description', 'channels',
            'reward_type', 'reward_value', 'reward_account', 'estimated_cost',
            'schedule_type', 'start_date', 'end_date', 'frequency_cap',
            'current_approver', 'approval_level', 'segment'
        ]

    def validate(self, data):
        """Validate campaign update data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("Start date cannot be after end date.")

        return data


class CampaignListItemSerializer(serializers.Serializer):
    """Serializer for individual campaign items in list response"""
    id = serializers.SerializerMethodField()
    name = serializers.CharField()
    type = serializers.SerializerMethodField()
    segment = serializers.SerializerMethodField()
    channels = serializers.ListField(child=serializers.CharField())
    status = serializers.SerializerMethodField()
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()

    def get_id(self, obj):
        # Return integer ID for frontend compatibility
        return obj.id.int if hasattr(obj.id, 'int') else hash(str(obj.id)) % 1000000

    def get_type(self, obj):
        # Return display name instead of value
        campaign_type_display = {
            'incentive': 'Incentive',
            'informational': 'Info',
            'win_back': 'Win-back',
            'info': 'Info'
        }
        return campaign_type_display.get(obj.campaign_type, obj.campaign_type)

    def get_segment(self, obj):
        return obj.segment.name if obj.segment else None

    def get_status(self, obj):
        # Return display name with proper capitalization
        status_display = {
            'draft': 'Draft',
            'pending_approval': 'Pending Approval',
            'scheduled': 'Scheduled',
            'running': 'Running',
            'paused': 'Paused',
            'completed': 'Completed',
            'failed': 'Failed',
            'cancelled': 'Cancelled'
        }
        return status_display.get(obj.status, obj.status)

    def get_startDate(self, obj):
        if obj.start_date:
            return obj.start_date.strftime('%Y-%m-%d')
        return None

    def get_endDate(self, obj):
        if obj.end_date:
            return obj.end_date.strftime('%Y-%m-%d')
        return None


class CampaignListSerializer(serializers.Serializer):
    """Serializer for campaign list response"""
    status = serializers.CharField(default="success")
    campaigns = CampaignSerializer(many=True)
    pagination = serializers.DictField()
    summary = serializers.DictField()


class ApprovalTrailSerializer(serializers.ModelSerializer):
    """Serializer for ApprovalTrail model"""
    approver_name = serializers.CharField(source='approver.username', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)

    class Meta:
        model = ApprovalTrail
        fields = [
            'id', 'campaign', 'campaign_name', 'approver', 'approver_name',
            'decision', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ReportConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for ReportConfiguration model"""
    configuration_display = serializers.SerializerMethodField()
    scheduling_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportConfiguration
        fields = [
            'id', 'name', 'description', 'source_type', 'configuration',
            'export_format', 'scheduling_enabled', 'frequency', 'recipients',
            'is_active', 'created_at', 'updated_at', 'configuration_display',
            'scheduling_display'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_configuration_display(self, obj):
        return obj.get_configuration_display()
    
    def get_scheduling_display(self, obj):
        return obj.get_scheduling_display()


class ReportConfigurationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating ReportConfiguration"""
    
    class Meta:
        model = ReportConfiguration
        fields = [
            'name', 'description', 'source_type', 'configuration',
            'export_format', 'scheduling_enabled', 'frequency', 'recipients',
            'is_active'
        ]
    
    def validate(self, data):
        """Validate configuration based on source_type"""
        source_type = data.get('source_type')
        configuration = data.get('configuration', {})
        
        if source_type == 'campaign':
            if not configuration.get('campaign_id'):
                raise serializers.ValidationError({
                    'configuration': 'campaign_id is required for campaign source type'
                })
        elif source_type == 'custom':
            custom_mode = configuration.get('custom_mode')
            if custom_mode == 'sql':
                if not configuration.get('sql_query'):
                    raise serializers.ValidationError({
                        'configuration': 'sql_query is required for custom SQL mode'
                    })
            elif custom_mode == 'filter':
                if not configuration.get('filters'):
                    raise serializers.ValidationError({
                        'configuration': 'filters are required for custom filter mode'
                    })
        
        # Validate scheduling
        if data.get('scheduling_enabled'):
            if not data.get('frequency'):
                raise serializers.ValidationError({
                    'frequency': 'Frequency is required when scheduling is enabled'
                })
            if not data.get('recipients'):
                raise serializers.ValidationError({
                    'recipients': 'Recipients are required when scheduling is enabled'
                })
        
        return data


class ReportConfigurationListSerializer(serializers.ModelSerializer):
    """Serializer for listing ReportConfigurations"""
    configuration_display = serializers.SerializerMethodField()
    scheduling_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportConfiguration
        fields = [
            'id', 'name', 'description', 'source_type', 'export_format',
            'scheduling_enabled', 'is_active', 'created_at', 'updated_at',
            'configuration_display', 'scheduling_display'
        ]
    
    def get_configuration_display(self, obj):
        return obj.get_configuration_display()
    
    def get_scheduling_display(self, obj):
        return obj.get_scheduling_display()
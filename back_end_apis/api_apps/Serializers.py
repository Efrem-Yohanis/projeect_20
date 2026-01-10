# api_apps/serializers.py
from rest_framework import serializers
from .models import CustomerSegment

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
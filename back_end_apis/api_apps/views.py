# api_apps/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mock_data import MockDataGenerator
from datetime import datetime

class CustomerMetricsAPI(APIView):
    """
    GET /api/dashboard/customer-metrics?period=30d
    Returns customer metrics for different time periods
    """
    
    def get(self, request):
        period = request.GET.get('period', '24h')
        
        # Validate period
        valid_periods = ['24h', '7d', '30d', '90d']
        if period not in valid_periods:
            return Response(
                {'error': f'Invalid period. Must be one of: {", ".join(valid_periods)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = MockDataGenerator.get_customer_metrics(period)
        return Response(data)

class ActivityTrendAPI(APIView):
    """
    GET /api/dashboard/activity-trend?period=7d
    Returns active vs dormant trend data
    """
    
    def get(self, request):
        period = request.GET.get('period', '7d')
        
        # Validate period
        valid_periods = ['7d', '30d', '90d']
        if period not in valid_periods:
            return Response(
                {'error': f'Invalid period. Must be one of: {", ".join(valid_periods)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = MockDataGenerator.get_activity_trend(period)
        return Response(data)

class ChurnRiskDistributionAPI(APIView):
    """
    GET /api/dashboard/churn-risk-distribution
    Returns churn risk distribution data
    """
    
    def get(self, request):
        data = MockDataGenerator.get_churn_risk_distribution()
        return Response(data)

class CampaignPerformanceAPI(APIView):
    """
    GET /api/dashboard/campaign-performance
    Returns campaign performance data
    """
    
    def get(self, request):
        data = MockDataGenerator.get_campaign_performance()
        return Response(data)

class RecentCampaignsAPI(APIView):
    """
    GET /api/dashboard/recent-campaigns
    Returns recent campaigns data
    """
    
    def get(self, request):
        data = MockDataGenerator.get_recent_campaigns()
        return Response(data)
# api_apps/views.py (update the DashboardSummaryAPI class)


class DashboardSummaryAPI(APIView):
    """
    GET /api/dashboard/summary?period=30d
    Returns complete dashboard data (all APIs combined)
    """
    
    def get(self, request):
        period = request.GET.get('period', '30d')
        
        # Determine trend period based on metrics period
        if period == '24h':
            trend_period = '7d'  # Default to weekly trend for daily metrics
        else:
            trend_period = period
        
        data = {
            'status': 'success',
            'period': period,
            'data': {
                'customer_metrics': MockDataGenerator.get_customer_metrics(period),
                'activity_trend': MockDataGenerator.get_activity_trend(trend_period),
                'churn_risk_distribution': MockDataGenerator.get_churn_risk_distribution(),
                'campaign_performance': MockDataGenerator.get_campaign_performance(),
                'recent_campaigns': MockDataGenerator.get_recent_campaigns()
            },
            'timestamp': datetime.now().isoformat() + 'Z'  # Fixed: Use datetime directly
        }
        
        return Response(data)
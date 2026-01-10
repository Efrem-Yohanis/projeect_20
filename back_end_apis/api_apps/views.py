# api_apps/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mock_data import MockDataGenerator
from datetime import datetime
from .models import CustomerSegment
from .Serializers import CustomerSegmentSerializer, SegmentListSerializer, CreateSegmentSerializer, SegmentListItemSerializer, UpdateSegmentSerializer
from django.core.paginator import Paginator
from django.utils import timezone

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


class SegmentListAPI(APIView):
    """
    GET /api/segments/
    Returns list of all customer segments with pagination and summary
    """

    def get(self, request):
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # Get all active segments
        segments = CustomerSegment.objects.filter(is_active=True).order_by('-last_refresh', '-created_at')

        # Pagination
        paginator = Paginator(segments, page_size)
        page_obj = paginator.get_page(page)

        # Serialize segments
        segment_serializer = SegmentListItemSerializer(page_obj.object_list, many=True)

        # Calculate summary
        total_customers = sum(seg.customer_count for seg in segments)
        last_updated = segments.first().last_refresh if segments.exists() else timezone.now()

        # Prepare response
        response_data = {
            "status": "success",
            "segments": segment_serializer.data,
            "pagination": {
                "total": paginator.count,
                "page": page,
                "page_size": page_size,
                "total_pages": paginator.num_pages
            },
            "summary": {
                "total_segments": paginator.count,
                "total_customers_in_segments": total_customers,
                "last_updated": last_updated.isoformat() + 'Z'
            }
        }

        return Response(response_data)


class SegmentCreateAPI(APIView):
    """
    POST /api/segments/create/
    Creates a new customer segment
    """

    def post(self, request):
        serializer = CreateSegmentSerializer(data=request.data)
        if serializer.is_valid():
            # Create segment
            segment = serializer.save()
            
            # Mock customer count (in real app, calculate based on criteria)
            import random
            segment.customer_count = random.randint(10000, 200000)
            segment.save()
            
            # Mock estimated preview (in real app, this would be calculated)
            estimated_preview = {
                "total_customers": segment.customer_count,
                "percent_of_base": round(random.uniform(5, 15), 1),
                "active_rate": random.randint(70, 90),
                "new_registrations": random.randint(5000, 20000),
                "high_value_percent": random.randint(20, 50),
                "estimated_refresh_time": "5-10 minutes"
            }

            # Serialize the created segment using full serializer
            segment_serializer = CustomerSegmentSerializer(segment)

            response_data = {
                "status": "success",
                "message": "Segment created successfully",
                "segment": segment_serializer.data,
                "estimated_preview": estimated_preview
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error",
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class SegmentDetailAPI(APIView):
    """
    GET /api/segments/<id>/ - Returns details of a specific segment
    PUT /api/segments/<id>/ - Updates a specific segment
    """

    def get(self, request, segment_id):
        # Use mock data for now
        result = MockDataGenerator.get_segment_detail(segment_id)
        return Response(result)
    
    def put(self, request, segment_id):
        try:
            segment = CustomerSegment.objects.get(id=segment_id, is_active=True)
        except CustomerSegment.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Segment not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateSegmentSerializer(segment, data=request.data, partial=True)
        if serializer.is_valid():
            # Update segment
            updated_segment = serializer.save()
            
            # Mock customer count update (in real app, recalculate based on new criteria)
            import random
            updated_segment.customer_count = random.randint(10000, 200000)
            updated_segment.save()
            
            # Serialize the updated segment
            segment_serializer = CustomerSegmentSerializer(updated_segment)
            
            response_data = {
                "status": "success",
                "message": "Segment updated successfully",
                "segment": segment_serializer.data
            }
            
            return Response(response_data)
        else:
            return Response({
                "status": "error",
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class SegmentDeleteAPI(APIView):
    """
    DELETE /api/segments/<id>/delete/
    Deletes a specific segment
    """

    def delete(self, request, segment_id):
        try:
            segment = CustomerSegment.objects.get(id=segment_id, is_active=True)
            segment.is_active = False  # Soft delete
            segment.save()
            return Response({
                "status": "success",
                "message": "Segment deleted successfully"
            })
        except CustomerSegment.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Segment not found"
            }, status=status.HTTP_404_NOT_FOUND)
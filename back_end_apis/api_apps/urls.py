# api_apps/urls.py
from django.urls import path
from .views import (
    CustomerMetricsAPI,
    ActivityTrendAPI,
    ChurnRiskDistributionAPI,
    CampaignPerformanceAPI,
    RecentCampaignsAPI,
    DashboardSummaryAPI,
    SegmentListAPI,
    SegmentCreateAPI,
    SegmentDetailAPI,
    SegmentDeleteAPI
)

urlpatterns = [
    # Individual APIs
    path('customer-metrics/', CustomerMetricsAPI.as_view(), name='customer-metrics'),
    path('activity-trend/', ActivityTrendAPI.as_view(), name='activity-trend'),
    path('churn-risk-distribution/', ChurnRiskDistributionAPI.as_view(), name='churn-risk-distribution'),
    path('campaign-performance/', CampaignPerformanceAPI.as_view(), name='campaign-performance'),
    path('recent-campaigns/', RecentCampaignsAPI.as_view(), name='recent-campaigns'),
    
    # Combined API
    path('summary/', DashboardSummaryAPI.as_view(), name='dashboard-summary'),

    # Segmentation APIs
    path('segments/', SegmentListAPI.as_view(), name='segment-list'),
    path('segments/create/', SegmentCreateAPI.as_view(), name='segment-create'),
    path('segments/<str:segment_id>/', SegmentDetailAPI.as_view(), name='segment-detail'),
    path('segments/<str:segment_id>/delete/', SegmentDeleteAPI.as_view(), name='segment-delete'),
]
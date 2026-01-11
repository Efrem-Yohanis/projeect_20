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
    SegmentDeleteAPI,
    RewardAccountListAPI,
    RewardAccountCreateAPI,
    RewardAccountDetailAPI,
    RewardAccountDeleteAPI,
    CampaignListAPI,
    CampaignCreateAPI,
    CampaignDetailAPI,
    CampaignDeleteAPI,
    CampaignApprovalAPI,
    CampaignSubmitAPI,
    CampaignApprovalTrailsAPI,
    CampaignAudienceAPI,
    CampaignChannelsAPI,
    CampaignRewardsAPI,
    CampaignPerformanceAPI as CampaignPerformanceTabAPI,
    CampaignLogsAPI
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

    # Reward Account APIs
    path('reward-accounts/', RewardAccountListAPI.as_view(), name='reward-account-list'),
    path('reward-accounts/create/', RewardAccountCreateAPI.as_view(), name='reward-account-create'),
    path('reward-accounts/<int:account_id>/', RewardAccountDetailAPI.as_view(), name='reward-account-detail'),
    path('reward-accounts/<int:account_id>/delete/', RewardAccountDeleteAPI.as_view(), name='reward-account-delete'),

    # Campaign APIs
    path('campaigns/', CampaignListAPI.as_view(), name='campaign-list'),
    path('campaigns/create/', CampaignCreateAPI.as_view(), name='campaign-create'),
    path('campaigns/<uuid:campaign_id>/', CampaignDetailAPI.as_view(), name='campaign-detail'),
    path('campaigns/<uuid:campaign_id>/delete/', CampaignDeleteAPI.as_view(), name='campaign-delete'),
    path('campaigns/<uuid:campaign_id>/approve/', CampaignApprovalAPI.as_view(), name='campaign-approve'),
    path('campaigns/<uuid:campaign_id>/submit/', CampaignSubmitAPI.as_view(), name='campaign-submit'),
    path('campaigns/<uuid:campaign_id>/approval-trails/', CampaignApprovalTrailsAPI.as_view(), name='campaign-approval-trails'),
    path('campaigns/<uuid:campaign_id>/audience/', CampaignAudienceAPI.as_view(), name='campaign-audience'),
    path('campaigns/<uuid:campaign_id>/channels/', CampaignChannelsAPI.as_view(), name='campaign-channels'),
    path('campaigns/<uuid:campaign_id>/rewards/', CampaignRewardsAPI.as_view(), name='campaign-rewards'),
    path('campaigns/<uuid:campaign_id>/performance/', CampaignPerformanceTabAPI.as_view(), name='campaign-performance-tab'),
    path('campaigns/<uuid:campaign_id>/logs/', CampaignLogsAPI.as_view(), name='campaign-logs'),
]
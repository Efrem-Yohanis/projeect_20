# api_apps/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mock_data import MockDataGenerator
from datetime import datetime
from .models import CustomerSegment, RewardAccount, Campaign, ApprovalTrail
from .Serializers import CustomerSegmentSerializer, SegmentListSerializer, CreateSegmentSerializer, SegmentListItemSerializer, UpdateSegmentSerializer, RewardAccountSerializer, RewardAccountCreateSerializer, RewardAccountUpdateSerializer, RewardAccountListSerializer, CampaignSerializer, CampaignCreateSerializer, CampaignUpdateSerializer, CampaignListItemSerializer, CampaignListSerializer, ApprovalTrailSerializer, ReportConfigurationSerializer, ReportConfigurationCreateSerializer, ReportConfigurationListSerializer
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

class CustomerViewAPI(APIView):
    """
    GET /api/customer/<customer_id>/
    Returns detailed customer profile and activity data
    """
    
    def get(self, request, customer_id):
        data = MockDataGenerator.get_customer_view(customer_id)
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


class RewardAccountListAPI(APIView):
    """
    GET /api/reward-accounts/
    Returns list of all reward accounts with pagination and summary
    """

    def get(self, request):
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # Get all reward accounts
        accounts = RewardAccount.objects.all().order_by('-created_at')

        # Pagination
        paginator = Paginator(accounts, page_size)
        page_obj = paginator.get_page(page)

        # Serialize accounts
        account_serializer = RewardAccountSerializer(page_obj.object_list, many=True)

        # Calculate summary
        total_balance = sum(account.balance for account in accounts)
        active_accounts = accounts.filter(status='active').count()
        total_accounts = accounts.count()

        # Prepare response
        response_data = {
            "status": "success",
            "accounts": account_serializer.data,
            "pagination": {
                "total": paginator.count,
                "page": page,
                "page_size": page_size,
                "total_pages": paginator.num_pages
            },
            "summary": {
                "total_accounts": total_accounts,
                "active_accounts": active_accounts,
                "total_balance": float(total_balance),
                "formatted_total_balance": f"{total_balance:,.2f} ETB"
            }
        }

        return Response(response_data)


class RewardAccountCreateAPI(APIView):
    """
    POST /api/reward-accounts/create/
    Creates a new reward account
    """

    def post(self, request):
        serializer = RewardAccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Create account
            account = serializer.save()

            # Serialize the created account
            account_serializer = RewardAccountSerializer(account)

            response_data = {
                "status": "success",
                "message": "Reward account created successfully",
                "account": account_serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error",
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class RewardAccountDetailAPI(APIView):
    """
    GET /api/reward-accounts/<id>/ - Returns details of a specific reward account
    PUT /api/reward-accounts/<id>/ - Updates a specific reward account
    """

    def get(self, request, account_id):
        try:
            account = RewardAccount.objects.get(id=account_id)
            serializer = RewardAccountSerializer(account)
            return Response({
                "status": "success",
                "account": serializer.data
            })
        except RewardAccount.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Reward account not found"
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, account_id):
        try:
            account = RewardAccount.objects.get(id=account_id)
        except RewardAccount.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Reward account not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = RewardAccountUpdateSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            # Update account
            updated_account = serializer.save()

            # Serialize the updated account
            account_serializer = RewardAccountSerializer(updated_account)

            response_data = {
                "status": "success",
                "message": "Reward account updated successfully",
                "account": account_serializer.data
            }

            return Response(response_data)
        else:
            return Response({
                "status": "error",
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class RewardAccountDeleteAPI(APIView):
    """
    DELETE /api/reward-accounts/<id>/delete/
    Deletes a specific reward account
    """

    def delete(self, request, account_id):
        try:
            account = RewardAccount.objects.get(id=account_id)
            account.delete()
            return Response({
                "status": "success",
                "message": "Reward account deleted successfully"
            })
        except RewardAccount.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Reward account not found"
            }, status=status.HTTP_404_NOT_FOUND)


class CampaignListAPI(APIView):
    """
    GET /api/campaigns/
    Returns list of all campaigns with pagination and summary
    """

    def get(self, request):
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        status_filter = request.GET.get('status')
        campaign_type = request.GET.get('campaign_type')

        # Get all campaigns
        campaigns = Campaign.objects.select_related('owner', 'current_approver', 'segment', 'reward_account').all().order_by('-created_at')

        # Apply filters
        if status_filter:
            campaigns = campaigns.filter(status=status_filter)
        if campaign_type:
            campaigns = campaigns.filter(campaign_type=campaign_type)

        # Pagination
        paginator = Paginator(campaigns, page_size)
        page_obj = paginator.get_page(page)

        # Serialize campaigns using the new format
        campaign_serializer = CampaignListItemSerializer(page_obj.object_list, many=True)

        # Calculate summary
        total_campaigns = campaigns.count()
        active_campaigns = campaigns.filter(status__in=['running', 'scheduled']).count()
        total_estimated_cost = sum(campaign.estimated_cost or 0 for campaign in campaigns)

        # Prepare response using CampaignListSerializer
        response_data = {
            "status": "success",
            "campaigns": campaign_serializer.data,
            "pagination": {
                "total": paginator.count,
                "page": page,
                "page_size": page_size,
                "total_pages": paginator.num_pages
            },
            "summary": {
                "total_campaigns": total_campaigns,
                "active_campaigns": active_campaigns,
                "total_estimated_cost": float(total_estimated_cost),
                "formatted_total_cost": f"{total_estimated_cost:,.2f} ETB"
            }
        }

        return Response(response_data)


class CampaignCreateAPI(APIView):
    """
    POST /api/campaigns/create/
    Creates a new campaign
    """

    def post(self, request):
        serializer = CampaignCreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Create campaign
            campaign = serializer.save()

            # Calculate estimated cost (simple calculation based on reward value and targeted customers)
            estimated_cost = 0
            if campaign.reward_value and campaign.total_targeted_customers:
                estimated_cost = float(campaign.reward_value) * campaign.total_targeted_customers

            # Update campaign with estimated cost
            campaign.estimated_cost = estimated_cost
            campaign.save()

            # Get account balance remaining (mock calculation)
            account_balance_remaining = 1000000 - estimated_cost  # Assuming 1M ETB budget

            # Check for conflicting campaigns (mock - no conflicts for now)
            conflicting_campaigns = 0

            # Determine approval workflow (mock logic)
            current_stage = "Department Head"
            next_approver = "Marketing Manager"

            # Format status for display
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

            response_data = {
                "success": True,
                "message": "Campaign submitted for approval successfully",
                "data": {
                    "campaignId": campaign.campaign_id,
                    "status": status_display.get(campaign.status, campaign.status),
                    "createdAt": campaign.created_at.isoformat() + 'Z',
                    "validationSummary": {
                        "estimatedCost": estimated_cost,
                        "accountBalanceRemaining": account_balance_remaining,
                        "conflictingCampaigns": conflicting_campaigns
                    },
                    "approvalWorkflow": {
                        "currentStage": current_stage,
                        "nextApprover": next_approver
                    }
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class CampaignDetailAPI(APIView):
    """
    GET /api/campaigns/<uuid>/ - Returns campaign header and overview
    PUT /api/campaigns/<uuid>/ - Updates a specific campaign
    """

    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.select_related('owner', 'current_approver', 'segment', 'reward_account').get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "success": False,
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Format status for display
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

        # Get approval trails
        approvals = []
        for trail in campaign.approval_trails.all().order_by('-created_at')[:5]:
            approvals.append({
                "status": trail.decision.title(),
                "comment": trail.comment,
                "date": trail.created_at.strftime("%Y-%m-%d %I:%M %p")
            })

        # Get channel configurations
        channels = []
        for i, channel in enumerate(campaign.channels or []):
            channel_config = campaign.channel_settings.get(channel.lower(), {})
            messages = campaign.messages.get(channel.lower(), {})

            channels.append({
                "type": channel.upper(),
                "enabled": True,
                "priority": i + 1,
                "cap": channel_config.get('cap', 100000),
                "content": [
                    {"lang": "English", "text": messages.get('en', f"Hello customer from {channel}!")},
                    {"lang": "Amharic", "text": messages.get('am', f"ሰላም የ{channel} ተጠቃሚ!")}
                ]
            })

        response_data = {
            "success": True,
            "campaignId": campaign.campaign_id,
            "data": {
                "header": {
                    "name": campaign.name,
                    "status": status_display.get(campaign.status, campaign.status),
                    "type": campaign.campaign_type.title() if campaign.campaign_type else "Incentive",
                    "owner": campaign.owner.username if campaign.owner else "Unknown",
                    "createdDate": campaign.created_at.strftime('%Y-%m-%d'),
                    "objective": campaign.objective
                },
                "overview": {
                    "summary": {
                        "description": campaign.description,
                        "scheduleType": campaign.schedule_type.title() if campaign.schedule_type else "Immediate",
                        "frequencyCap": campaign.frequency_cap.replace('_', ' ').title() if campaign.frequency_cap else "Unlimited"
                    },
                    "rewards": {
                        "type": campaign.reward_type.title() if campaign.reward_type else "Other",
                        "value": f"{campaign.reward_value} ETB" if campaign.reward_value else "0 ETB",
                        "dailyCap": f"{campaign.reward_caps.get('perDay', 500)} ETB",
                        "perCustomerCap": f"{campaign.reward_caps.get('perCustomer', 2000)} ETB",
                        "account": campaign.reward_account.account_name if campaign.reward_account else "Main Rewards Pool",
                        "estimatedCost": f"{campaign.estimated_cost or 0:,.0f} ETB"
                    },
                    "channels": channels,
                    "approvals": approvals
                }
            }
        }

        return Response(response_data)

    def put(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "success": False,
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CampaignUpdateSerializer(campaign, data=request.data, partial=True)
        if serializer.is_valid():
            # Update campaign
            updated_campaign = serializer.save()

            # Serialize the updated campaign
            campaign_serializer = CampaignSerializer(updated_campaign)

            response_data = {
                "success": True,
                "message": "Campaign updated successfully",
                "data": campaign_serializer.data
            }

            return Response(response_data)
        else:
            return Response({
                "success": False,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class CampaignAudienceAPI(APIView):
    """
    GET /api/campaigns/<uuid>/audience/ - Returns campaign audience stats and list
    """

    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.select_related('segment').get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "success": False,
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        total_customers = campaign.total_targeted_customers or 45000

        # Mock audience stats
        stats = {
            "total": total_customers,
            "segments": [
                {"label": "Active", "count": int(total_customers * 0.85), "percentage": 85},
                {"label": "Dormant", "count": int(total_customers * 0.15), "percentage": 15}
            ],
            "valueTiers": [
                {"label": "High Value", "count": int(total_customers * 0.4), "percentage": 40},
                {"label": "Medium Value", "count": int(total_customers * 0.35), "percentage": 35},
                {"label": "Low Value", "count": int(total_customers * 0.25), "percentage": 25}
            ]
        }

        # Mock customer list
        import random
        customer_list = []
        statuses = ["Active", "Dormant", "Inactive"]
        tiers = ["High", "Medium", "Low"]
        risks = ["Low", "Medium", "High"]
        rewards = ["Received", "Pending", "Failed"]

        for i in range(min(50, total_customers)):  # Show max 50 customers
            customer_list.append({
                "msisdn": f"2519****{random.randint(1000, 9999)}",
                "tier": random.choice(tiers),
                "status": random.choice(statuses),
                "risk": random.choice(risks),
                "reward": random.choice(rewards)
            })

        response_data = {
            "success": True,
            "data": {
                "stats": stats,
                "list": customer_list
            }
        }

        return Response(response_data)


class CampaignChannelsAPI(APIView):
    """
    GET /api/campaigns/<uuid>/channels/ - Returns campaign channel configuration and metrics
    """

    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "success": False,
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        channels_data = []
        for channel in campaign.channels or ["SMS"]:
            channel_config = campaign.channel_settings.get(channel.lower(), {})
            messages = campaign.messages.get(channel.lower(), {})

            # Mock metrics
            targeted = campaign.total_targeted_customers or 45000
            sent = int(targeted * 0.98)
            delivered = int(sent * 0.94)
            failed = sent - delivered

            channels_data.append({
                "type": channel.upper(),
                "status": "Enabled",
                "configuration": {
                    "templates": {
                        "english": messages.get('en', f"Hello customer from {channel}!"),
                        "amharic": messages.get('am', f"ሰላም የ{channel} ተጠቃሚ!")
                    },
                    "characterCount": len(messages.get('en', f"Hello customer from {channel}!"))
                },
                "metrics": {
                    "sent": sent,
                    "delivered": delivered,
                    "failed": failed
                }
            })

        response_data = {
            "success": True,
            "data": {
                "channels": channels_data
            }
        }

        return Response(response_data)


class CampaignRewardsAPI(APIView):
    """
    GET /api/campaigns/<uuid>/rewards/ - Returns campaign reward configuration and status
    """

    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.select_related('reward_account').get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "success": False,
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Mock reward account details
        starting_balance = 500000
        consumed = campaign.estimated_cost or 385000
        current_balance = starting_balance - consumed

        # Mock status log
        import random
        status_log = []
        reasons = ["Insufficient balance", "Invalid account", "Technical error", "Success"]
        statuses = ["Success", "Failed", "Pending"]

        for i in range(10):
            status_log.append({
                "msisdn": f"2519****{random.randint(1000, 9999)}",
                "status": random.choice(statuses),
                "reason": random.choice(reasons),
                "timestamp": f"2024-01-{random.randint(1, 15):02d} {random.randint(9, 17):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
            })

        response_data = {
            "success": True,
            "data": {
                "configuration": {
                    "type": campaign.reward_type.title() if campaign.reward_type else "Cashback",
                    "value": f"{campaign.reward_value} ETB" if campaign.reward_value else "10 ETB",
                    "campaignCap": f"{campaign.reward_caps.get('campaignCap', 500000):,} ETB"
                },
                "accountDetails": {
                    "id": campaign.reward_account.account_id if campaign.reward_account else "RWD-ACC-001",
                    "name": campaign.reward_account.account_name if campaign.reward_account else "Festive Rewards Pool",
                    "currentBalance": current_balance,
                    "consumed": consumed,
                    "startingBalance": starting_balance
                },
                "statusLog": status_log
            }
        }

        return Response(response_data)


class CampaignPerformanceAPI(APIView):
    """
    GET /api/campaigns/<uuid>/performance/ - Returns campaign performance KPIs and trends
    """

    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "success": False,
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Mock KPIs
        kpis = [
            {"label": "Conversion Rate", "value": "12.4%", "icon": "TrendingUp", "color": "success"},
            {"label": "Reach Rate", "value": "94.1%", "icon": "Users", "color": "info"},
            {"label": "Engagement Rate", "value": "8.7%", "icon": "Activity", "color": "warning"},
            {"label": "ROI", "value": "2.3x", "icon": "DollarSign", "color": "success"}
        ]

        # Mock daily trend
        import random
        daily_trend = []
        base_targeted = campaign.total_targeted_customers or 45000
        days = 7

        for i in range(days):
            targeted = int(base_targeted / days * (0.9 + random.uniform(-0.1, 0.1)))
            activated = int(targeted * 0.58 * (0.9 + random.uniform(-0.1, 0.1)))

            daily_trend.append({
                "date": f"Jan {i+1}",
                "targeted": targeted,
                "activated": activated
            })

        # Mock channel performance
        channel_performance = []
        for channel in campaign.channels or ["SMS", "Push", "Email"]:
            targeted = campaign.total_targeted_customers or 45000
            sent = int(targeted * 0.98)
            delivered = int(sent * (0.91 + random.uniform(-0.02, 0.02)))
            success_rate = round((delivered / targeted * 100), 1) if targeted > 0 else 0

            channel_performance.append({
                "channel": channel.upper(),
                "targeted": targeted,
                "sent": sent,
                "delivered": delivered,
                "successRate": success_rate
            })

        response_data = {
            "success": True,
            "data": {
                "kpis": kpis,
                "dailyTrend": daily_trend,
                "channelPerformance": channel_performance
            }
        }

        return Response(response_data)


class CampaignLogsAPI(APIView):
    """
    GET /api/campaigns/<uuid>/logs/ - Returns campaign system logs and audit trail
    """

    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.select_related('owner').get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "success": False,
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Mock system logs
        system_logs = [
            {"timestamp": "2024-01-15 10:25:01", "type": "error", "message": "SMS gateway timeout"},
            {"timestamp": "2024-01-15 10:20:01", "type": "info", "message": "Campaign started successfully"},
            {"timestamp": "2024-01-15 09:15:01", "type": "warning", "message": "Low balance warning"},
            {"timestamp": "2024-01-14 16:30:01", "type": "info", "message": "Approval workflow completed"}
        ]

        # Mock audit trail
        audit_trail = []
        for trail in campaign.approval_trails.all().order_by('-created_at'):
            audit_trail.append({
                "timestamp": trail.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "user": trail.approver.username,
                "action": f"Campaign {trail.decision.title()}"
            })

        # Add some mock audit entries if none exist
        if not audit_trail:
            audit_trail = [
                {"timestamp": "2024-01-01 14:00:00", "user": campaign.owner.username if campaign.owner else "System", "action": "Campaign Created"},
                {"timestamp": "2024-01-01 15:30:00", "user": "Jane D.", "action": "Campaign Submitted"},
                {"timestamp": "2024-01-02 09:15:00", "user": "Mike R.", "action": "Campaign Approved"}
            ]

        response_data = {
            "success": True,
            "data": {
                "systemLogs": system_logs,
                "auditTrail": audit_trail
            }
        }

        return Response(response_data)


class CampaignDeleteAPI(APIView):
    """
    DELETE /api/campaigns/<uuid>/delete/
    Deletes a specific campaign
    """

    def delete(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            campaign.delete()
            return Response({
                "status": "success",
                "message": "Campaign deleted successfully"
            })
        except Campaign.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)


class CampaignApprovalAPI(APIView):
    """
    POST /api/campaigns/<uuid>/approve/
    Approves or rejects a campaign
    """

    def post(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        decision = request.data.get('decision')
        comment = request.data.get('comment', '')
        approver_id = request.data.get('approver_id')

        if decision not in ['approved', 'rejected']:
            return Response({
                "status": "error",
                "message": "Decision must be 'approved' or 'rejected'"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create approval trail
        approval_trail = ApprovalTrail.objects.create(
            campaign=campaign,
            approver_id=approver_id,
            decision=decision,
            comment=comment
        )

        # Update campaign status based on decision
        if decision == 'approved':
            # Simple approval logic - in real app, this would be more complex
            campaign.status = 'scheduled'
            campaign.current_approver = None
        else:
            campaign.status = 'draft'
            campaign.current_approver = None

        campaign.save()

        return Response({
            "status": "success",
            "message": f"Campaign {decision} successfully",
            "approval_trail": ApprovalTrailSerializer(approval_trail).data
        })


class CampaignSubmitAPI(APIView):
    """
    POST /api/campaigns/<uuid>/submit/
    Submits a campaign for approval
    """

    def post(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if campaign.status != 'draft':
            return Response({
                "status": "error",
                "message": "Only draft campaigns can be submitted for approval"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update campaign status
        campaign.status = 'pending_approval'
        campaign.submitted_on = timezone.now()
        campaign.save()

        return Response({
            "status": "success",
            "message": "Campaign submitted for approval successfully"
        })


class CampaignApprovalTrailsAPI(APIView):
    """
    GET /api/campaigns/<uuid>/approval-trails/
    Returns approval trails for a specific campaign
    """

    def get(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Campaign not found"
            }, status=status.HTTP_404_NOT_FOUND)

        approval_trails = campaign.approval_trails.all().order_by('-created_at')
        serializer = ApprovalTrailSerializer(approval_trails, many=True)

        return Response({
            "status": "success",
            "approval_trails": serializer.data
        })


class ReportConfigurationListAPI(APIView):
    """
    GET /api/report-configurations/
    POST /api/report-configurations/
    List all report configurations or create a new one
    """
    
    def get(self, request):
        configurations = MockDataGenerator.get_report_configurations()
        return Response({
            "status": "success",
            "count": len(configurations),
            "results": configurations
        })
    
    def post(self, request):
        serializer = ReportConfigurationCreateSerializer(data=request.data)
        if serializer.is_valid():
            # In a real implementation, this would save to database
            # For now, we'll just return the validated data
            data = serializer.validated_data
            data['id'] = str(uuid.uuid4())
            data['created_at'] = timezone.now().isoformat()
            data['updated_at'] = timezone.now().isoformat()
            
            return Response({
                "status": "success",
                "message": "Report configuration created successfully",
                "data": data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ReportConfigurationDetailAPI(APIView):
    """
    GET /api/report-configurations/<uuid:config_id>/
    PUT /api/report-configurations/<uuid:config_id>/
    DELETE /api/report-configurations/<uuid:config_id>/
    Retrieve, update, or delete a report configuration
    """
    
    def get(self, request, config_id):
        configuration = MockDataGenerator.get_report_configuration(config_id)
        if not configuration:
            return Response({
                "status": "error",
                "message": "Report configuration not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "status": "success",
            "data": configuration
        })
    
    def put(self, request, config_id):
        configuration = MockDataGenerator.get_report_configuration(config_id)
        if not configuration:
            return Response({
                "status": "error",
                "message": "Report configuration not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReportConfigurationCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Update the configuration
            data = serializer.validated_data
            data['id'] = config_id
            data['created_at'] = configuration['created_at']
            data['updated_at'] = timezone.now().isoformat()
            
            return Response({
                "status": "success",
                "message": "Report configuration updated successfully",
                "data": data
            })
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, config_id):
        configuration = MockDataGenerator.get_report_configuration(config_id)
        if not configuration:
            return Response({
                "status": "error",
                "message": "Report configuration not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # In a real implementation, this would delete from database
        return Response({
            "status": "success",
            "message": "Report configuration deleted successfully"
        })


class ReportsListAPI(APIView):
    """
    GET /api/reports/ - Returns list of reports with pagination
    POST /api/reports/ - Creates a new report
    """
    
    def get(self, request):
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10
        
        data = MockDataGenerator.get_reports_list(page=page, page_size=page_size)
        return Response(data)
    
    def post(self, request):
        """Create a new report"""
        data = request.data
        
        # Validate required fields
        required_fields = ['name', 'source_type', 'source_config', 'export_format']
        for field in required_fields:
            if field not in data:
                return Response({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate source_type
        if data['source_type'] not in ['campaign', 'custom']:
            return Response({
                'success': False,
                'message': 'source_type must be either "campaign" or "custom"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate source_config based on source_type
        source_config = data['source_config']
        if data['source_type'] == 'campaign':
            if not source_config.get('campaign_id'):
                return Response({
                    'success': False,
                    'message': 'campaign_id is required for campaign source_type'
                }, status=status.HTTP_400_BAD_REQUEST)
        elif data['source_type'] == 'custom':
            custom_mode = source_config.get('custom_mode')
            if custom_mode not in ['sql', 'filter']:
                return Response({
                    'success': False,
                    'message': 'custom_mode must be either "sql" or "filter"'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if custom_mode == 'sql' and not source_config.get('sql_query'):
                return Response({
                    'success': False,
                    'message': 'sql_query is required for custom SQL mode'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if custom_mode == 'filter' and not source_config.get('filters'):
                return Response({
                    'success': False,
                    'message': 'filters are required for custom filter mode'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate export_format
        if data['export_format'] not in ['pdf', 'excel', 'csv']:
            return Response({
                'success': False,
                'message': 'export_format must be one of: pdf, excel, csv'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate scheduling if provided
        scheduling = data.get('scheduling', {})
        if scheduling.get('enabled'):
            if not scheduling.get('frequency'):
                return Response({
                    'success': False,
                    'message': 'frequency is required when scheduling is enabled'
                }, status=status.HTTP_400_BAD_REQUEST)
            if not scheduling.get('recipients'):
                return Response({
                    'success': False,
                    'message': 'recipients are required when scheduling is enabled'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate report ID
        import random
        report_id = f"rpt-{random.randint(1000, 9999)}"
        
        # Create response
        from datetime import datetime
        created_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        response_data = {
            'success': True,
            'message': 'Report created and queued for generation.',
            'data': {
                'id': report_id,
                'name': data['name'],
                'status': 'pending',
                'created_at': created_at
            }
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class ReportDetailAPI(APIView):
    """
    GET /api/reports/:id - Returns detailed information about a specific report
    PUT /api/reports/:id - Updates an existing report
    """

    def get(self, request, report_id):
        # Get detailed report data
        report_data = MockDataGenerator.get_report_detail(report_id)

        if not report_data:
            return Response({
                'success': False,
                'message': f'Report with ID {report_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'data': report_data
        })

    def put(self, request, report_id):
        """Update an existing report"""
        data = request.data

        # Check if report exists
        existing_report = MockDataGenerator.get_report_detail(report_id)
        if not existing_report:
            return Response({
                'success': False,
                'message': f'Report with ID {report_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Validate source_type if provided
        if 'source_type' in data:
            if data['source_type'] not in ['campaign', 'custom']:
                return Response({
                    'success': False,
                    'message': 'source_type must be either "campaign" or "custom"'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Validate source_config if provided
        if 'source_config' in data:
            source_config = data['source_config']
            source_type = data.get('source_type', existing_report['source_type'])

            if source_type == 'campaign':
                if not source_config.get('campaign_id'):
                    return Response({
                        'success': False,
                        'message': 'campaign_id is required for campaign source_type'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif source_type == 'custom':
                custom_mode = source_config.get('custom_mode')
                if custom_mode not in ['sql', 'filter']:
                    return Response({
                        'success': False,
                        'message': 'custom_mode must be either "sql" or "filter"'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if custom_mode == 'sql' and not source_config.get('sql_query'):
                    return Response({
                        'success': False,
                        'message': 'sql_query is required for custom SQL mode'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if custom_mode == 'filter' and not source_config.get('filters'):
                    return Response({
                        'success': False,
                        'message': 'filters are required for custom filter mode'
                    }, status=status.HTTP_400_BAD_REQUEST)

        # Validate export_format if provided
        if 'export_format' in data:
            if data['export_format'] not in ['pdf', 'excel', 'csv']:
                return Response({
                    'success': False,
                    'message': 'export_format must be one of: pdf, excel, csv'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Validate scheduling if provided
        if 'scheduling' in data:
            scheduling = data['scheduling']
            if scheduling.get('enabled'):
                if not scheduling.get('frequency'):
                    return Response({
                        'success': False,
                        'message': 'frequency is required when scheduling is enabled'
                    }, status=status.HTTP_400_BAD_REQUEST)
                if not scheduling.get('recipients'):
                    return Response({
                        'success': False,
                        'message': 'recipients are required when scheduling is enabled'
                    }, status=status.HTTP_400_BAD_REQUEST)

        # Update the report
        updated_report = MockDataGenerator.update_report_detail(report_id, data)

        return Response({
            'success': True,
            'message': 'Report updated successfully.',
            'data': updated_report
        })
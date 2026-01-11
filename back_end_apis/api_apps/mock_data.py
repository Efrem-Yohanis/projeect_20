# api_apps/mock_data.py
from datetime import datetime, timedelta
import json

class MockDataGenerator:
    """Centralized mock data generator for all APIs"""
    
    @staticmethod
    def get_customer_metrics(period='24h'):
        """Generate customer metrics mock data"""
        now = datetime.now()
        
        data_templates = {
            '24h': {
                'period': '24h',
                'metrics': {
                    'total_customers': {'current': 2400000, 'previous': 2398000, 'change': 0.1, 'threshold': None},
                    'active_customers': {'current': 65000, 'previous': 62000, 'change': 4.8, 'threshold': 1},
                    'new_registered': {'current': 1800, 'previous': 1700, 'change': 5.9, 'threshold': None},
                    'churn_rate': {'current': 0.2, 'previous': 0.3, 'change': -33.3, 'threshold': None},
                    'dormant_customers': {'current': 420000, 'previous': 421000, 'change': -0.2, 'threshold': 90}
                },
                'days': 1
            },
            '7d': {
                'period': '7d',
                'metrics': {
                    'total_customers': {'current': 2400000, 'previous': 2380000, 'change': 0.8, 'threshold': None},
                    'active_customers': {'current': 450000, 'previous': 435000, 'change': 3.4, 'threshold': 7},
                    'new_registered': {'current': 12500, 'previous': 11500, 'change': 8.7, 'threshold': None},
                    'churn_rate': {'current': 1.2, 'previous': 1.4, 'change': -14.3, 'threshold': None},
                    'dormant_customers': {'current': 420000, 'previous': 422000, 'change': -0.5, 'threshold': 90}
                },
                'days': 7
            },
            '30d': {
                'period': '30d',
                'metrics': {
                    'total_customers': {'current': 2400000, 'previous': 2285714, 'change': 5.2, 'threshold': None},
                    'active_customers': {'current': 1800000, 'previous': 1746000, 'change': 3.1, 'threshold': 30},
                    'new_registered': {'current': 52000, 'previous': 46222, 'change': 12.5, 'threshold': None},
                    'churn_rate': {'current': 4.2, 'previous': 5.0, 'change': -0.8, 'threshold': None},
                    'dormant_customers': {'current': 420000, 'previous': 430000, 'change': -2.4, 'threshold': 90}
                },
                'days': 30
            },
            '90d': {
                'period': '90d',
                'metrics': {
                    'total_customers': {'current': 2400000, 'previous': 2200000, 'change': 9.1, 'threshold': None},
                    'active_customers': {'current': 1850000, 'previous': 1750000, 'change': 5.7, 'threshold': 30},
                    'new_registered': {'current': 155000, 'previous': 135000, 'change': 14.8, 'threshold': None},
                    'churn_rate': {'current': 12.5, 'previous': 13.8, 'change': -9.4, 'threshold': None},
                    'dormant_customers': {'current': 420000, 'previous': 445000, 'change': -5.6, 'threshold': 90}
                },
                'days': 90
            }
        }
        
        template = data_templates.get(period, data_templates['24h'])
        
        # Format numbers
        def format_number(num):
            if num >= 1000000:
                return f"{num/1000000:.1f}M"
            elif num >= 1000:
                return f"{num/1000:.0f}K"
            return str(num)
        
        def format_percentage(num):
            return f"{num:.1f}%"
        
        # Build metrics response
        metrics = {}
        for key, values in template['metrics'].items():
            metric_data = {
                'current': values['current'],
                'formatted': format_number(values['current']) if key != 'churn_rate' else format_percentage(values['current']),
                'previous_period': values['previous'],
                'change': values['change'],
                'change_type': 'increase' if values['change'] >= 0 else 'decrease'
            }
            
            # Add threshold_days for specific metrics
            if values['threshold'] is not None:
                metric_data['threshold_days'] = values['threshold']
            
            metrics[key] = metric_data
        
        # Calculate date ranges
        days = template['days']
        current_end = now
        current_start = now - timedelta(days=days)
        previous_end = current_start
        previous_start = previous_end - timedelta(days=days)
        
        return {
            'status': 'success',
            'period': template['period'],
            'metrics': metrics,
            'date_ranges': {
                'current_period_start': current_start.isoformat() + 'Z',
                'current_period_end': current_end.isoformat() + 'Z',
                'previous_period_start': previous_start.isoformat() + 'Z',
                'previous_period_end': previous_end.isoformat() + 'Z'
            },
            'updated_at': now.isoformat() + 'Z'
        }
    
    @staticmethod
    def get_activity_trend(period='7d'):
        """Generate activity trend mock data"""
        now = datetime.now()
        
        templates = {
            '7d': {
                'granularity': 'daily',
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'active_data': [8500, 9200, 7800, 9500, 8800, 7600, 8200],
                'dormant_data': [4200, 3800, 4500, 3500, 4000, 4200, 3900],
                'days': 7
            },
            '30d': {
                'granularity': 'daily',
                'labels': [str(i+1) for i in range(30)],
                'active_data': [8200, 8400, 8600, 8300, 8500, 8700, 8900, 8800, 9000, 9200,
                               9100, 9300, 9400, 9200, 9500, 9600, 9400, 9700, 9800, 9600,
                               9500, 9700, 9800, 9900, 10000, 9800, 9700, 9900, 10000, 10200],
                'dormant_data': [4100, 4050, 4000, 3950, 3900, 3850, 3800, 3750, 3700, 3650,
                                 3600, 3550, 3500, 3450, 3400, 3350, 3300, 3250, 3200, 3150,
                                 3100, 3050, 3000, 2950, 2900, 2850, 2800, 2750, 2700, 2650],
                'days': 30
            },
            '90d': {
                'granularity': 'weekly',
                'labels': [f'Week {i+1}' for i in range(12)],
                'active_data': [55000, 56000, 57000, 58000, 59000, 60000, 
                               61000, 62000, 63000, 64000, 65000, 66000],
                'dormant_data': [15000, 14500, 14000, 13500, 13000, 12500,
                                12000, 11500, 11000, 10500, 10000, 9500],
                'days': 90
            }
        }
        
        template = templates.get(period, templates['7d'])
        
        total_active = sum(template['active_data'])
        total_dormant = sum(template['dormant_data'])
        total = total_active + total_dormant
        
        start_date = now - timedelta(days=template['days'])
        
        return {
            'status': 'success',
            'period': period,
            'chart_type': 'line',
            'granularity': template['granularity'],
            'labels': template['labels'],
            'datasets': [
                {
                    'label': 'Active Users',
                    'data': template['active_data'],
                    'borderColor': '#3b82f6',
                    'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                    'fill': True,
                    'tension': 0.4
                },
                {
                    'label': 'Dormant Users',
                    'data': template['dormant_data'],
                    'borderColor': '#ef4444',
                    'backgroundColor': 'rgba(239, 68, 68, 0.1)',
                    'fill': True,
                    'tension': 0.4
                }
            ],
            'totals': {
                'total_active': total_active,
                'total_dormant': total_dormant,
                'active_percentage': round((total_active / total * 100), 1) if total > 0 else 0,
                'dormant_percentage': round((total_dormant / total * 100), 1) if total > 0 else 0
            },
            'date_ranges': {
                'start_date': start_date.isoformat() + 'Z',
                'end_date': now.isoformat() + 'Z'
            },
            'updated_at': now.isoformat() + 'Z'
        }
    
    @staticmethod
    def get_churn_risk_distribution():
        """Generate churn risk distribution mock data"""
        now = datetime.now()
        
        return {
            'status': 'success',
            'analysis': {
                'timestamp': now.isoformat() + 'Z',
                'timeframe': 'last_30_days',
                'total_customers_analyzed': 2400000,
                'distribution': {
                    'low_risk': {
                        'count': 18450,
                        'percentage': 65,
                        'description': 'Customers with low probability of churning'
                    },
                    'medium_risk': {
                        'count': 8100,
                        'percentage': 28.5,
                        'description': 'Customers showing some risk indicators'
                    },
                    'high_risk': {
                        'count': 2450,
                        'percentage': 8.6,
                        'description': 'Customers at high risk of churning',
                        'recommendation': 'Launch win-back campaign'
                    }
                },
                'summary': {
                    'total_at_high_risk': 2450,
                    'high_risk_percentage': 8.6,
                    'key_insight': '2,450 customers require immediate attention'
                }
            }
        }
    
    @staticmethod
    def get_campaign_performance():
        """Generate campaign performance mock data"""
        now = datetime.now()
        
        return {
            'status': 'success',
            'campaigns': [
                {
                    'id': 'campaign_1',
                    'name': 'Win-back Q4',
                    'performance': 45000,
                    'target': 60000,
                    'completion_rate': 75,
                    'color': '#8b5cf6'
                },
                {
                    'id': 'campaign_2',
                    'name': 'Festive Bonus',
                    'performance': 38000,
                    'target': 45000,
                    'completion_rate': 84.4,
                    'color': '#3b82f6'
                },
                {
                    'id': 'campaign_3',
                    'name': 'New User',
                    'performance': 52000,
                    'target': 30000,
                    'completion_rate': 173.3,
                    'color': '#10b981'
                },
                {
                    'id': 'campaign_4',
                    'name': 'Loyalty Tier',
                    'performance': 28000,
                    'target': 15000,
                    'completion_rate': 186.7,
                    'color': '#f59e0b'
                }
            ],
            'timeframe': 'Q4 2024',
            'total_performance': 163000,
            'average_completion_rate': 129.85,
            'updated_at': now.isoformat() + 'Z'
        }
    
    @staticmethod
    def get_recent_campaigns():
        """Generate recent campaigns mock data"""
        now = datetime.now()
        
        return {
            'status': 'success',
            'campaigns': [
                {
                    'id': 'campaign_001',
                    'name': 'Meskel Season Rewards',
                    'delivered': 42300,
                    'target': 45000,
                    'progress': 94,
                    'status': 'running',
                    'start_date': '2024-09-27T00:00:00Z',
                    'end_date': '2024-10-05T23:59:59Z',
                    'type': 'seasonal'
                },
                {
                    'id': 'campaign_002',
                    'name': 'Timket Win-back',
                    'delivered': 25600,
                    'target': 28000,
                    'progress': 91.4,
                    'status': 'running',
                    'start_date': '2024-01-05T00:00:00Z',
                    'end_date': '2024-01-20T23:59:59Z',
                    'type': 'retention'
                },
                {
                    'id': 'campaign_003',
                    'name': 'Genna Alert',
                    'delivered': 148500,
                    'target': 150000,
                    'progress': 99,
                    'status': 'completed',
                    'start_date': '2023-12-20T00:00:00Z',
                    'end_date': '2024-01-07T23:59:59Z',
                    'type': 'holiday'
                }
            ],
            'total_running': 2,
            'total_completed': 1,
            'overall_delivery_rate': 94.8,
            'updated_at': now.isoformat() + 'Z'
        }

    @staticmethod
    def get_segments_list(search=None, page=1, page_size=10):
        """Get list of customer segments with search and pagination"""
        now = datetime.now()
        
        # Mock segments data
        segments = [
            {
                'id': 'seg_001',
                'name': 'High Value Active Users',
                'description': 'Active customers with high lifetime value',
                'customer_count': 125000,
                'last_refresh': now.replace(hour=14, minute=30).isoformat() + 'Z',
                'created_at': '2024-01-10T09:15:00Z',
                'updated_at': now.replace(hour=14, minute=30).isoformat() + 'Z',
                'segment_type': 'behavioral',
                'criteria': {
                    'status': 'active',
                    'lifetime_value_min': 1000,
                    'last_active_days_max': 30
                },
                'metadata': {
                    'color': '#10b981',
                    'icon': 'dollar-sign',
                    'priority': 'high'
                },
                'is_active': True,
                'is_system': False
            },
            {
                'id': 'seg_002',
                'name': 'Dormant 30 Days',
                'description': 'Customers inactive for 30+ days',
                'customer_count': 89500,
                'last_refresh': now.replace(hour=14, minute=30).isoformat() + 'Z',
                'created_at': '2024-01-05T11:20:00Z',
                'updated_at': now.replace(hour=14, minute=30).isoformat() + 'Z',
                'segment_type': 'activity',
                'criteria': {
                    'last_active_days_min': 30,
                    'status': ['active', 'inactive']
                },
                'metadata': {
                    'color': '#f59e0b',
                    'icon': 'moon',
                    'priority': 'medium'
                },
                'is_active': True,
                'is_system': False
            },
            {
                'id': 'seg_003',
                'name': 'New Users Dec 2023',
                'description': 'Users registered in December 2023',
                'customer_count': 45200,
                'last_refresh': now.replace(hour=9, minute=0).isoformat() + 'Z',
                'created_at': '2024-01-01T08:00:00Z',
                'updated_at': now.replace(hour=9, minute=0).isoformat() + 'Z',
                'segment_type': 'demographic',
                'criteria': {
                    'registration_date_from': '2023-12-01',
                    'registration_date_to': '2023-12-31'
                },
                'metadata': {
                    'color': '#3b82f6',
                    'icon': 'user-plus',
                    'priority': 'low'
                },
                'is_active': True,
                'is_system': True
            },
            {
                'id': 'seg_004',
                'name': 'Churn Risk High',
                'description': 'Customers at high risk of churning',
                'customer_count': 24500,
                'last_refresh': now.replace(hour=12, minute=0).isoformat() + 'Z',
                'created_at': '2024-01-08T10:45:00Z',
                'updated_at': now.replace(hour=12, minute=0).isoformat() + 'Z',
                'segment_type': 'risk',
                'criteria': {
                    'churn_risk': 'high',
                    'engagement_score_max': 30,
                    'last_active_days_min': 15
                },
                'metadata': {
                    'color': '#ef4444',
                    'icon': 'alert-triangle',
                    'priority': 'high'
                },
                'is_active': True,
                'is_system': True
            },
            {
                'id': 'seg_005',
                'name': 'Premium Subscribers',
                'description': 'Active premium subscription users',
                'customer_count': 35600,
                'last_refresh': now.replace(hour=10, minute=15).isoformat() + 'Z',
                'created_at': '2024-01-12T14:20:00Z',
                'updated_at': now.replace(hour=10, minute=15).isoformat() + 'Z',
                'segment_type': 'value',
                'criteria': {
                    'subscription_tier': 'premium',
                    'subscription_active': True,
                    'status': 'active'
                },
                'metadata': {
                    'color': '#8b5cf6',
                    'icon': 'crown',
                    'priority': 'medium'
                },
                'is_active': True,
                'is_system': False
            }
        ]
        
        # Apply search filter if provided
        if search:
            segments = [s for s in segments if search.lower() in s['name'].lower()]
        
        # Apply pagination
        total = len(segments)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_segments = segments[start_idx:end_idx]
        
        # Add formatted count and action
        for segment in paginated_segments:
            segment['formatted_customer_count'] = f"{segment['customer_count']:,}"
            segment['action'] = 'view'
        
        # Calculate summary
        total_customers = sum(s['customer_count'] for s in segments)
        last_updated = max(s['last_refresh'] for s in segments) if segments else now.isoformat() + 'Z'
        
        return {
            'status': 'success',
            'segments': paginated_segments,
            'pagination': {
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            },
            'summary': {
                'total_segments': total,
                'total_customers_in_segments': total_customers,
                'last_updated': last_updated
            }
        }
    
    @staticmethod
    def get_segment_detail(segment_id):
        """Get detailed information for a specific segment"""
        segments = MockDataGenerator.get_segments_list()['segments']
        
        # Find the segment
        segment = next((s for s in segments if s['id'] == segment_id), None)
        
        if not segment:
            return {
                'status': 'error',
                'message': 'Segment not found'
            }
        
        # Map segment_type to display name
        type_mapping = {
            'behavioral': 'Behavioral',
            'demographic': 'Demographic',
            'activity': 'Activity',
            'risk': 'Risk',
            'value': 'Value',
            'custom': 'Custom'
        }
        
        # Add detailed information matching the UI
        segment_detail = {
            **segment,
            'type': type_mapping.get(segment.get('segment_type', 'custom'), 'Custom'),
            'last_refreshed': segment['last_refresh'][:19].replace('T', ' '),  # Format as 2024-01-15 14:30
            'new_users_30d': {
                'count': 4520,
                'percentage': 3.6
            },
            'value_distribution': {
                'high': 35,
                'medium': 45,
                'low': 20
            },
            'churn_risk': {
                'count': 8500,
                'avg_probability': 32
            },
            'customer_preview': [
                {
                    'msisdn': '2547****123',
                    'reg_date': '2023-06-15',
                    'last_activity': '2024-01-14',
                    'txn_count_30d': 45,
                    'txn_value_30d': 'KES 78,500',
                    'value_tier': 'High',
                    'churn_risk': 'Low'
                },
                {
                    'msisdn': '2547****456',
                    'reg_date': '2023-08-22',
                    'last_activity': '2024-01-15',
                    'txn_count_30d': 32,
                    'txn_value_30d': 'KES 52,000',
                    'value_tier': 'High',
                    'churn_risk': 'Low'
                },
                {
                    'msisdn': '2547****789',
                    'reg_date': '2023-03-10',
                    'last_activity': '2024-01-10',
                    'txn_count_30d': 18,
                    'txn_value_30d': 'KES 25,000',
                    'value_tier': 'Medium',
                    'churn_risk': 'Medium'
                },
                # Add more mock customers to make 10
                {
                    'msisdn': '2547****101',
                    'reg_date': '2023-07-05',
                    'last_activity': '2024-01-13',
                    'txn_count_30d': 28,
                    'txn_value_30d': 'KES 41,200',
                    'value_tier': 'Medium',
                    'churn_risk': 'Low'
                },
                {
                    'msisdn': '2547****202',
                    'reg_date': '2023-09-18',
                    'last_activity': '2024-01-12',
                    'txn_count_30d': 12,
                    'txn_value_30d': 'KES 18,900',
                    'value_tier': 'Low',
                    'churn_risk': 'High'
                },
                {
                    'msisdn': '2547****303',
                    'reg_date': '2023-05-22',
                    'last_activity': '2024-01-11',
                    'txn_count_30d': 55,
                    'txn_value_30d': 'KES 95,000',
                    'value_tier': 'High',
                    'churn_risk': 'Low'
                },
                {
                    'msisdn': '2547****404',
                    'reg_date': '2023-11-30',
                    'last_activity': '2024-01-09',
                    'txn_count_30d': 8,
                    'txn_value_30d': 'KES 12,500',
                    'value_tier': 'Low',
                    'churn_risk': 'High'
                },
                {
                    'msisdn': '2547****505',
                    'reg_date': '2023-04-14',
                    'last_activity': '2024-01-08',
                    'txn_count_30d': 41,
                    'txn_value_30d': 'KES 67,800',
                    'value_tier': 'High',
                    'churn_risk': 'Medium'
                },
                {
                    'msisdn': '2547****606',
                    'reg_date': '2023-10-08',
                    'last_activity': '2024-01-07',
                    'txn_count_30d': 22,
                    'txn_value_30d': 'KES 33,400',
                    'value_tier': 'Medium',
                    'churn_risk': 'Medium'
                },
                {
                    'msisdn': '2547****707',
                    'reg_date': '2023-12-01',
                    'last_activity': '2024-01-06',
                    'txn_count_30d': 15,
                    'txn_value_30d': 'KES 22,100',
                    'value_tier': 'Low',
                    'churn_risk': 'High'
                }
            ]
        }
        
        return {
            'status': 'success',
            'segment': segment_detail
        }
    
    @staticmethod
    def create_segment(segment_data):
        """Create a new segment (mock)"""
        now = datetime.now()
        
        # Generate new segment ID
        segment_id = f"seg_{now.strftime('%Y%m%d%H%M%S')}"
        
        new_segment = {
            'id': segment_id,
            'name': segment_data.get('name', 'New Segment'),
            'description': segment_data.get('description', ''),
            'customer_count': 0,
            'last_refresh': now.isoformat() + 'Z',
            'created_at': now.isoformat() + 'Z',
            'updated_at': now.isoformat() + 'Z',
            'segment_type': segment_data.get('segment_type', 'custom'),
            'criteria': segment_data.get('criteria', {}),
            'metadata': segment_data.get('metadata', {}),
            'formatted_customer_count': '0',
            'action': 'view',
            'is_active': True,
            'is_system': False
        }
        
        return {
            'status': 'success',
            'message': 'Segment created successfully',
            'segment': new_segment
        }
    
    @staticmethod
    def refresh_segment(segment_id):
        """Refresh segment customer count (mock)"""
        now = datetime.now()
        
        # Simulate count update
        import random
        new_count = random.randint(1000, 150000)
        
        return {
            'status': 'success',
            'message': 'Segment refreshed successfully',
            'segment_id': segment_id,
            'new_customer_count': new_count,
            'formatted_customer_count': f"{new_count:,}",
            'last_refresh': now.isoformat() + 'Z'
        }
    
    @staticmethod
    def get_report_configurations():
        """Generate mock report configurations"""
        return [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Monthly Campaign Performance Report",
                "description": "Comprehensive monthly report on campaign performance metrics",
                "source_type": "campaign",
                "configuration": {
                    "campaign_id": "camp-1"
                },
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly",
                    "recipients": ["manager@company.com", "analyst@company.com"]
                },
                "is_active": True,
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-15T14:30:00Z"
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "name": "Customer Churn Analysis",
                "description": "Weekly analysis of customer churn patterns and risk factors",
                "source_type": "custom",
                "configuration": {
                    "custom_mode": "filter",
                    "filters": [
                        {
                            "field": "churn_score",
                            "operator": "greater_than",
                            "value": "70"
                        },
                        {
                            "field": "last_active",
                            "operator": "less_than",
                            "value": "30"
                        }
                    ]
                },
                "export_format": "excel",
                "scheduling": {
                    "enabled": True,
                    "frequency": "weekly",
                    "recipients": ["churn-team@company.com"]
                },
                "is_active": True,
                "created_at": "2024-01-05T09:00:00Z",
                "updated_at": "2024-01-10T11:15:00Z"
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440003",
                "name": "Revenue Analytics Dashboard",
                "description": "Daily revenue metrics and trends analysis",
                "source_type": "custom",
                "configuration": {
                    "custom_mode": "sql",
                    "sql_query": "SELECT DATE(transaction_date) as date, SUM(amount) as revenue FROM transactions WHERE transaction_date >= '2024-01-01' GROUP BY DATE(transaction_date) ORDER BY date DESC"
                },
                "export_format": "csv",
                "scheduling": {
                    "enabled": True,
                    "frequency": "daily",
                    "recipients": ["finance@company.com", "ceo@company.com"]
                },
                "is_active": True,
                "created_at": "2024-01-08T08:30:00Z",
                "updated_at": "2024-01-12T16:45:00Z"
            }
        ]
    
    @staticmethod
    def get_report_configuration(report_id):
        """Get a specific report configuration by ID"""
        configurations = MockDataGenerator.get_report_configurations()
        for config in configurations:
            if config['id'] == report_id:
                return config
        return None
        """Generate customer view mock data"""
        # Mock customer data based on the provided expected response
        customers = {
            '254712456789': {
                "profile": {
                    "msisdn": "254712456789",
                    "name": "Jane Wanjiku",
                    "initials": "JW",
                    "status": "Active",
                    "tier": "Gold",
                    "kycLevel": "Full KYC",
                    "demographics": {
                        "gender": "Female",
                        "age": 32,
                        "region": "Nairobi",
                        "city": "Westlands"
                    },
                    "dates": {
                        "registered": "2021-03-15",
                        "lastActive": "2024-01-15T14:32:00Z"
                    }
                },
                "metrics": {
                    "lifetimeValue": 245000,
                    "monthlyAvg": 12500,
                    "currency": "KES"
                },
                "aiInsights": {
                    "churnScore": 15,
                    "churnRisk": "Low",
                    "recommendedAction": "Offer tier upgrade to Platinum"
                },
                "activities": {
                    "transactions": [
                        {
                            "id": "tx_101",
                            "date": "2024-01-15 14:32",
                            "type": "Send Money",
                            "amount": 2500,
                            "status": "Completed"
                        },
                        {
                            "id": "tx_102",
                            "date": "2024-01-14 09:15",
                            "type": "Pay Bill",
                            "amount": 5000,
                            "status": "Completed"
                        }
                    ],
                    "campaigns": [
                        {
                            "id": "cmp_501",
                            "name": "Festive Rewards",
                            "date": "2024-01-05",
                            "status": "Delivered",
                            "reward": "KES 50"
                        }
                    ],
                    "messages": [
                        {
                            "id": "msg_901",
                            "date": "2024-01-15",
                            "channel": "SMS",
                            "content": "Your M-Pesa balance is..."
                        }
                    ]
                }
            }
        }
        
        # Return customer data if exists, otherwise return a default mock
        return customers.get(customer_id, {
            "profile": {
                "msisdn": customer_id,
                "name": "John Doe",
                "initials": "JD",
                "status": "Active",
                "tier": "Silver",
                "kycLevel": "Basic KYC",
                "demographics": {
                    "gender": "Male",
                    "age": 28,
                    "region": "Nairobi",
                    "city": "CBD"
                },
                "dates": {
                    "registered": "2022-05-20",
                    "lastActive": "2024-01-10T10:15:00Z"
                }
            },
            "metrics": {
                "lifetimeValue": 150000,
                "monthlyAvg": 8500,
                "currency": "KES"
            },
            "aiInsights": {
                "churnScore": 35,
                "churnRisk": "Medium",
                "recommendedAction": "Send engagement campaign"
            },
            "activities": {
                "transactions": [
                    {
                        "id": "tx_201",
                        "date": "2024-01-10 10:15",
                        "type": "Buy Airtime",
                        "amount": 1000,
                        "status": "Completed"
                    }
                ],
                "campaigns": [],
                "messages": [
                    {
                        "id": "msg_801",
                        "date": "2024-01-08",
                        "channel": "SMS",
                        "content": "Welcome to our loyalty program!"
                    }
                ]
            }
        })
    
    @staticmethod
    def get_reports_list(page=1, page_size=10):
        """Generate mock reports list with pagination"""
        all_reports = [
            {
                "id": "rpt-001",
                "name": "Q4 Revenue Analysis",
                "description": "A detailed breakdown of revenue by region and product line for the final quarter.",
                "source_type": "campaign",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2024-01-10T10:00:00Z"
            },
            {
                "id": "rpt-002",
                "name": "Customer Churn SQL Export",
                "description": "Raw data export of high-risk customers based on custom SQL query.",
                "source_type": "custom",
                "export_format": "csv",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2024-01-11T14:30:00Z"
            },
            {
                "id": "rpt-003",
                "name": "Weekly Active Users",
                "description": None,
                "source_type": "campaign",
                "export_format": "excel",
                "scheduling": {
                    "enabled": True,
                    "frequency": "weekly"
                },
                "created_at": "2024-01-12T09:15:00Z"
            },
            {
                "id": "rpt-004",
                "name": "Monthly Transaction Summary",
                "description": "Summary of all transactions grouped by type and region.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2024-01-08T16:45:00Z"
            },
            {
                "id": "rpt-005",
                "name": "Campaign ROI Analysis",
                "description": "Return on investment analysis for all completed campaigns.",
                "source_type": "campaign",
                "export_format": "excel",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2024-01-09T11:20:00Z"
            },
            {
                "id": "rpt-006",
                "name": "Daily User Activity Report",
                "description": "Daily breakdown of user activities and engagement metrics.",
                "source_type": "custom",
                "export_format": "csv",
                "scheduling": {
                    "enabled": True,
                    "frequency": "daily"
                },
                "created_at": "2024-01-13T08:00:00Z"
            },
            {
                "id": "rpt-007",
                "name": "Quarterly Business Review",
                "description": "Comprehensive quarterly business performance review.",
                "source_type": "campaign",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2024-01-07T14:10:00Z"
            },
            {
                "id": "rpt-008",
                "name": "Customer Segmentation Export",
                "description": "Export of customer segments with detailed demographics.",
                "source_type": "custom",
                "export_format": "excel",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2024-01-06T12:30:00Z"
            },
            {
                "id": "rpt-009",
                "name": "Weekly Churn Risk Alert",
                "description": "Weekly report on customers at risk of churning.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "weekly"
                },
                "created_at": "2024-01-05T09:45:00Z"
            },
            {
                "id": "rpt-010",
                "name": "Annual Performance Summary",
                "description": "Year-end summary of all key performance indicators.",
                "source_type": "campaign",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2024-01-04T15:20:00Z"
            },
            # Add more reports to reach 25 total
            {
                "id": "rpt-011",
                "name": "Regional Sales Report",
                "description": "Sales performance by region and branch.",
                "source_type": "custom",
                "export_format": "excel",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2024-01-03T10:15:00Z"
            },
            {
                "id": "rpt-012",
                "name": "Customer Feedback Analysis",
                "description": "Analysis of customer feedback and satisfaction scores.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2024-01-02T13:40:00Z"
            },
            {
                "id": "rpt-013",
                "name": "Marketing Campaign Effectiveness",
                "description": "Effectiveness analysis of marketing campaigns.",
                "source_type": "campaign",
                "export_format": "excel",
                "scheduling": {
                    "enabled": True,
                    "frequency": "weekly"
                },
                "created_at": "2024-01-01T11:25:00Z"
            },
            {
                "id": "rpt-014",
                "name": "Product Usage Statistics",
                "description": "Statistics on product usage and adoption rates.",
                "source_type": "custom",
                "export_format": "csv",
                "scheduling": {
                    "enabled": True,
                    "frequency": "daily"
                },
                "created_at": "2023-12-31T16:50:00Z"
            },
            {
                "id": "rpt-015",
                "name": "Financial Reconciliation Report",
                "description": "Monthly financial reconciliation and variance analysis.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2023-12-30T14:35:00Z"
            },
            {
                "id": "rpt-016",
                "name": "User Onboarding Metrics",
                "description": "Metrics and analysis of user onboarding process.",
                "source_type": "custom",
                "export_format": "excel",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2023-12-29T12:10:00Z"
            },
            {
                "id": "rpt-017",
                "name": "Service Quality Report",
                "description": "Report on service quality and response times.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "weekly"
                },
                "created_at": "2023-12-28T09:55:00Z"
            },
            {
                "id": "rpt-018",
                "name": "Competitor Analysis",
                "description": "Analysis of competitor performance and market share.",
                "source_type": "custom",
                "export_format": "excel",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2023-12-27T15:40:00Z"
            },
            {
                "id": "rpt-019",
                "name": "Risk Assessment Report",
                "description": "Comprehensive risk assessment for business operations.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2023-12-26T13:25:00Z"
            },
            {
                "id": "rpt-020",
                "name": "Employee Performance Review",
                "description": "Quarterly review of employee performance metrics.",
                "source_type": "custom",
                "export_format": "excel",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2023-12-25T11:05:00Z"
            },
            {
                "id": "rpt-021",
                "name": "Inventory Management Report",
                "description": "Weekly inventory levels and management analysis.",
                "source_type": "custom",
                "export_format": "csv",
                "scheduling": {
                    "enabled": True,
                    "frequency": "weekly"
                },
                "created_at": "2023-12-24T08:50:00Z"
            },
            {
                "id": "rpt-022",
                "name": "Supplier Performance",
                "description": "Analysis of supplier performance and reliability.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": False,
                    "frequency": None
                },
                "created_at": "2023-12-23T14:30:00Z"
            },
            {
                "id": "rpt-023",
                "name": "Market Research Summary",
                "description": "Summary of latest market research findings.",
                "source_type": "custom",
                "export_format": "excel",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2023-12-22T12:15:00Z"
            },
            {
                "id": "rpt-024",
                "name": "Compliance Audit Report",
                "description": "Quarterly compliance audit and findings report.",
                "source_type": "custom",
                "export_format": "pdf",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2023-12-21T10:00:00Z"
            },
            {
                "id": "rpt-025",
                "name": "IT Security Incident Report",
                "description": "Monthly report on IT security incidents and responses.",
                "source_type": "custom",
                "export_format": "excel",
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly"
                },
                "created_at": "2023-12-20T16:45:00Z"
            }
        ]
        
        # Apply pagination
        total = len(all_reports)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_reports = all_reports[start_idx:end_idx]
        
        total_pages = (total + page_size - 1) // page_size
        
        return {
            "reports": paginated_reports,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        }
    
    @staticmethod
    def get_report_detail(report_id):
        """Generate detailed report data for a specific report ID"""
        
        # Mock detailed reports data
        detailed_reports = {
            "rpt-001": {
                "id": "rpt-001",
                "name": "Q4 Revenue Analysis",
                "description": "A detailed breakdown of revenue by region and product line for the final quarter.",
                "source_type": "custom",
                "export_format": "pdf",
                "created_at": "2024-01-10T10:00:00Z",
                "configuration": {
                    "custom_mode": "filter",
                    "campaign_id": None,
                    "sql_query": None,
                    "filters": [
                        {
                            "field": "transaction_value",
                            "operator": "greater_than",
                            "value": "1000"
                        },
                        {
                            "field": "region",
                            "operator": "equals",
                            "value": "North America"
                        }
                    ]
                },
                "scheduling": {
                    "enabled": True,
                    "frequency": "monthly",
                    "recipients": ["finance-team@company.com", "exec-office@company.com"]
                },
                "history": [
                    {
                        "date": "2024-01-15 09:00",
                        "status": "Success",
                        "size": "2.4 MB",
                        "duration": "45s",
                        "download_url": "/api/reports/download/file-abc.pdf"
                    },
                    {
                        "date": "2024-01-08 09:00",
                        "status": "Success",
                        "size": "2.1 MB",
                        "duration": "42s",
                        "download_url": "/api/reports/download/file-def.pdf"
                    }
                ]
            },
            "rpt-002": {
                "id": "rpt-002",
                "name": "Customer Segmentation Report",
                "description": "Analysis of customer segments based on behavior and demographics.",
                "source_type": "campaign",
                "export_format": "excel",
                "created_at": "2024-01-12T14:30:00Z",
                "configuration": {
                    "custom_mode": None,
                    "campaign_id": "camp-123",
                    "sql_query": None,
                    "filters": []
                },
                "scheduling": {
                    "enabled": False,
                    "frequency": None,
                    "recipients": []
                },
                "history": [
                    {
                        "date": "2024-01-14 10:15",
                        "status": "Success",
                        "size": "1.8 MB",
                        "duration": "32s",
                        "download_url": "/api/reports/download/file-ghi.xlsx"
                    }
                ]
            },
            "rpt-003": {
                "id": "rpt-003",
                "name": "Custom SQL Analytics",
                "description": "Advanced analytics using custom SQL queries for detailed insights.",
                "source_type": "custom",
                "export_format": "csv",
                "created_at": "2024-01-15T09:15:00Z",
                "configuration": {
                    "custom_mode": "sql",
                    "campaign_id": None,
                    "sql_query": "SELECT region, SUM(revenue) as total_revenue FROM transactions WHERE date >= '2024-01-01' GROUP BY region ORDER BY total_revenue DESC",
                    "filters": []
                },
                "scheduling": {
                    "enabled": True,
                    "frequency": "weekly",
                    "recipients": ["data-team@company.com"]
                },
                "history": [
                    {
                        "date": "2024-01-16 08:30",
                        "status": "Success",
                        "size": "950 KB",
                        "duration": "28s",
                        "download_url": "/api/reports/download/file-jkl.csv"
                    },
                    {
                        "date": "2024-01-09 08:30",
                        "status": "Failed",
                        "size": None,
                        "duration": "15s",
                        "download_url": None
                    }
                ]
            }
        }
        
        return detailed_reports.get(report_id)
    
    @staticmethod
    def update_report_detail(report_id, update_data):
        """Update an existing report with new data"""
        
        # Get existing report
        existing_report = MockDataGenerator.get_report_detail(report_id)
        if not existing_report:
            return None
        
        # Create updated report by merging existing data with updates
        updated_report = existing_report.copy()
        
        # Update basic fields
        if 'name' in update_data:
            updated_report['name'] = update_data['name']
        if 'description' in update_data:
            updated_report['description'] = update_data['description']
        if 'source_type' in update_data:
            updated_report['source_type'] = update_data['source_type']
        if 'export_format' in update_data:
            updated_report['export_format'] = update_data['export_format']
        
        # Update configuration
        if 'source_config' in update_data:
            config = update_data['source_config']
            updated_report['configuration'] = {
                'custom_mode': config.get('custom_mode'),
                'campaign_id': config.get('campaign_id'),
                'sql_query': config.get('sql_query'),
                'filters': config.get('filters', [])
            }
        
        # Update scheduling
        if 'scheduling' in update_data:
            scheduling = update_data['scheduling']
            updated_report['scheduling'] = {
                'enabled': scheduling.get('enabled', False),
                'frequency': scheduling.get('frequency'),
                'recipients': scheduling.get('recipients', [])
            }
        
        # Note: In a real implementation, this would persist to database
        # For now, we'll just return the updated data
        
        return updated_report
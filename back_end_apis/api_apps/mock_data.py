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
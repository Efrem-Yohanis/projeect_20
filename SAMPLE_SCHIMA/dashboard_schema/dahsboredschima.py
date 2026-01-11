{
  "api_endpoints": {
    "customer_metrics": {
      "method": "GET",
      "endpoint": "/api/dashboard/customer-metrics/",
      "description": "Get customer metrics data for dashboard",
      "query_parameters": {
        "period": {
          "type": "string",
          "enum": ["24h", "7d", "30d", "90d"],
          "default": "24h",
          "description": "Time period for metrics"
        }
      },
      "response": {
        "status": "success",
        "period": "30d",
        "metrics": {
          "total_customers": {
            "current": 2400000,
            "formatted": "2.4M",
            "previous_period": 2285714,
            "change": 5.2,
            "change_type": "increase"
          },
          "active_customers": {
            "current": 1800000,
            "formatted": "1.8M",
            "previous_period": 1746000,
            "change": 3.1,
            "change_type": "increase",
            "threshold_days": 30
          },
          "new_registered": {
            "current": 52000,
            "formatted": "52K",
            "previous_period": 46222,
            "change": 12.5,
            "change_type": "increase"
          },
          "churn_rate": {
            "current": 4.2,
            "formatted": "4.2%",
            "previous_period": 5.0,
            "change": -0.8,
            "change_type": "decrease"
          },
          "dormant_customers": {
            "current": 420000,
            "formatted": "420K",
            "previous_period": 430000,
            "change": -2.4,
            "change_type": "decrease",
            "threshold_days": 90
          }
        },
        "date_ranges": {
          "current_period_start": "2024-09-01T12:00:00Z",
          "current_period_end": "2024-10-01T12:00:00Z",
          "previous_period_start": "2024-08-02T12:00:00Z",
          "previous_period_end": "2024-09-01T12:00:00Z"
        },
        "updated_at": "2024-10-01T12:00:00Z"
      }
    },
    "activity_trend": {
      "method": "GET",
      "endpoint": "/api/dashboard/activity-trend/",
      "description": "Get activity trend data for dashboard charts",
      "query_parameters": {
        "period": {
          "type": "string",
          "enum": ["7d", "30d", "90d"],
          "default": "7d",
          "description": "Time period for trend data"
        }
      },
      "response": {
        "status": "success",
        "period": "30d",
        "chart_type": "line",
        "granularity": "daily",
        "labels": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"],
        "datasets": [
          {
            "label": "Active Users",
            "data": [8200, 8400, 8600, 8300, 8500, 8700, 8900, 8800, 9000, 9200, 9100, 9300, 9400, 9200, 9500, 9600, 9400, 9700, 9800, 9600, 9500, 9700, 9800, 9900, 10000, 9800, 9700, 9900, 10000, 10200],
            "borderColor": "#3b82f6",
            "backgroundColor": "rgba(59, 130, 246, 0.1)",
            "fill": true,
            "tension": 0.4
          },
          {
            "label": "Dormant Users",
            "data": [4100, 4050, 4000, 3950, 3900, 3850, 3800, 3750, 3700, 3650, 3600, 3550, 3500, 3450, 3400, 3350, 3300, 3250, 3200, 3150, 3100, 3050, 3000, 2950, 2900, 2850, 2800, 2750, 2700, 2650],
            "borderColor": "#ef4444",
            "backgroundColor": "rgba(239, 68, 68, 0.1)",
            "fill": true,
            "tension": 0.4
          }
        ],
        "totals": {
          "total_active": 275000,
          "total_dormant": 57500,
          "active_percentage": 82.7,
          "dormant_percentage": 17.3
        },
        "date_ranges": {
          "start_date": "2024-09-01T12:00:00Z",
          "end_date": "2024-10-01T12:00:00Z"
        },
        "updated_at": "2024-10-01T12:00:00Z"
      }
    },
    "churn_risk_distribution": {
      "method": "GET",
      "endpoint": "/api/dashboard/churn-risk-distribution/",
      "description": "Get churn risk distribution analysis",
      "response": {
        "status": "success",
        "analysis": {
          "timestamp": "2024-10-01T12:00:00Z",
          "timeframe": "last_30_days",
          "total_customers_analyzed": 2400000,
          "distribution": {
            "low_risk": {
              "count": 18450,
              "percentage": 65,
              "description": "Customers with low probability of churning"
            },
            "medium_risk": {
              "count": 8100,
              "percentage": 28.5,
              "description": "Customers showing some risk indicators"
            },
            "high_risk": {
              "count": 2450,
              "percentage": 8.6,
              "description": "Customers at high risk of churning",
              "recommendation": "Launch win-back campaign"
            }
          },
          "summary": {
            "total_at_high_risk": 2450,
            "high_risk_percentage": 8.6,
            "key_insight": "2,450 customers require immediate attention"
          }
        }
      }
    },
    "campaign_performance": {
      "method": "GET",
      "endpoint": "/api/dashboard/campaign-performance/",
      "description": "Get campaign performance metrics",
      "response": {
        "status": "success",
        "campaigns": [
          {
            "id": "campaign_1",
            "name": "Win-back Q4",
            "performance": 45000,
            "target": 60000,
            "completion_rate": 75,
            "color": "#8b5cf6"
          },
          {
            "id": "campaign_2",
            "name": "Festive Bonus",
            "performance": 38000,
            "target": 45000,
            "completion_rate": 84.4,
            "color": "#3b82f6"
          },
          {
            "id": "campaign_3",
            "name": "New User",
            "performance": 52000,
            "target": 30000,
            "completion_rate": 173.3,
            "color": "#10b981"
          },
          {
            "id": "campaign_4",
            "name": "Loyalty Tier",
            "performance": 28000,
            "target": 15000,
            "completion_rate": 186.7,
            "color": "#f59e0b"
          }
        ],
        "timeframe": "Q4 2024",
        "total_performance": 163000,
        "average_completion_rate": 129.85,
        "updated_at": "2024-10-01T12:00:00Z"
      }
    },
    "recent_campaigns": {
      "method": "GET",
      "endpoint": "/api/dashboard/recent-campaigns/",
      "description": "Get recent campaigns data",
      "response": {
        "status": "success",
        "campaigns": [
          {
            "id": "campaign_001",
            "name": "Meskel Season Rewards",
            "delivered": 42300,
            "target": 45000,
            "progress": 94,
            "status": "running",
            "start_date": "2024-09-27T00:00:00Z",
            "end_date": "2024-10-05T23:59:59Z",
            "type": "seasonal"
          },
          {
            "id": "campaign_002",
            "name": "Timket Win-back",
            "delivered": 25600,
            "target": 28000,
            "progress": 91.4,
            "status": "running",
            "start_date": "2024-01-05T00:00:00Z",
            "end_date": "2024-01-20T23:59:59Z",
            "type": "retention"
          },
          {
            "id": "campaign_003",
            "name": "Genna Alert",
            "delivered": 148500,
            "target": 150000,
            "progress": 99,
            "status": "completed",
            "start_date": "2023-12-20T00:00:00Z",
            "end_date": "2024-01-07T23:59:59Z",
            "type": "holiday"
          }
        ],
        "total_running": 2,
        "total_completed": 1,
        "overall_delivery_rate": 94.8,
        "updated_at": "2024-10-01T12:00:00Z"
      }
    },
    "dashboard_summary": {
      "method": "GET",
      "endpoint": "/api/dashboard/summary/",
      "description": "Get complete dashboard data (all APIs combined)",
      "query_parameters": {
        "period": {
          "type": "string",
          "enum": ["24h", "7d", "30d", "90d"],
          "default": "30d",
          "description": "Time period for metrics and trends"
        }
      },
      "response": {
        "status": "success",
        "period": "30d",
        "data": {
          "customer_metrics": {},
          "activity_trend": {},
          "churn_risk_distribution": {},
          "campaign_performance": {},
          "recent_campaigns": {}
        },
        "timestamp": "2024-10-01T12:00:00Z"
      }
    }
  },
  "data_models": {
    "CustomerMetrics": {
      "period": "string",
      "metrics": {
        "total_customers": {
          "current": "integer",
          "formatted": "string",
          "previous_period": "integer",
          "change": "float",
          "change_type": "string"
        },
        "active_customers": {
          "current": "integer",
          "formatted": "string",
          "previous_period": "integer",
          "change": "float",
          "change_type": "string",
          "threshold_days": "integer"
        },
        "new_registered": {
          "current": "integer",
          "formatted": "string",
          "previous_period": "integer",
          "change": "float",
          "change_type": "string"
        },
        "churn_rate": {
          "current": "float",
          "formatted": "string",
          "previous_period": "float",
          "change": "float",
          "change_type": "string"
        },
        "dormant_customers": {
          "current": "integer",
          "formatted": "string",
          "previous_period": "integer",
          "change": "float",
          "change_type": "string",
          "threshold_days": "integer"
        }
      },
      "date_ranges": {
        "current_period_start": "datetime",
        "current_period_end": "datetime",
        "previous_period_start": "datetime",
        "previous_period_end": "datetime"
      },
      "updated_at": "datetime"
    },
    "ActivityTrend": {
      "period": "string",
      "chart_type": "string",
      "granularity": "string",
      "labels": ["string"],
      "datasets": [
        {
          "label": "string",
          "data": ["integer"],
          "borderColor": "string",
          "backgroundColor": "string",
          "fill": "boolean",
          "tension": "float"
        }
      ],
      "totals": {
        "total_active": "integer",
        "total_dormant": "integer",
        "active_percentage": "float",
        "dormant_percentage": "float"
      },
      "date_ranges": {
        "start_date": "datetime",
        "end_date": "datetime"
      },
      "updated_at": "datetime"
    },
    "ChurnRiskDistribution": {
      "analysis": {
        "timestamp": "datetime",
        "timeframe": "string",
        "total_customers_analyzed": "integer",
        "distribution": {
          "low_risk": {
            "count": "integer",
            "percentage": "float",
            "description": "string"
          },
          "medium_risk": {
            "count": "integer",
            "percentage": "float",
            "description": "string"
          },
          "high_risk": {
            "count": "integer",
            "percentage": "float",
            "description": "string",
            "recommendation": "string"
          }
        },
        "summary": {
          "total_at_high_risk": "integer",
          "high_risk_percentage": "float",
          "key_insight": "string"
        }
      }
    },
    "CampaignPerformance": {
      "campaigns": [
        {
          "id": "string",
          "name": "string",
          "performance": "integer",
          "target": "integer",
          "completion_rate": "float",
          "color": "string"
        }
      ],
      "timeframe": "string",
      "total_performance": "integer",
      "average_completion_rate": "float",
      "updated_at": "datetime"
    },
    "RecentCampaigns": {
      "campaigns": [
        {
          "id": "string",
          "name": "string",
          "delivered": "integer",
          "target": "integer",
          "progress": "float",
          "status": "string",
          "start_date": "datetime",
          "end_date": "datetime",
          "type": "string"
        }
      ],
      "total_running": "integer",
      "total_completed": "integer",
      "overall_delivery_rate": "float",
      "updated_at": "datetime"
    }
  }
}

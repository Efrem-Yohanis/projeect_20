{
  "api_endpoints": {
    "list_segments": {
      "method": "GET",
      "endpoint": "/api/segments/",
      "description": "Get list of all segments with pagination",
      "response": {
        "status": "success",
        "segments": [
          {
            "id": "seg_001",
            "name": "High Value Active Users",
            "description": "Active customers with high lifetime value",
            "customer_count": 125000,
            "formatted_customer_count": "125,000",
            "last_refresh": "2024-01-15T14:30:00Z",
            "created_at": "2024-01-10T09:15:00Z",
            "updated_at": "2024-01-15T14:30:00Z",
            "segment_type": "behavioral",
            "criteria": {
              "status": "active",
              "lifetime_value_min": 1000,
              "last_active_days_max": 30
            }
          },
          {
            "id": "seg_002",
            "name": "Dormant 30 Days",
            "description": "Customers inactive for 30+ days",
            "customer_count": 89500,
            "formatted_customer_count": "89,500",
            "last_refresh": "2024-01-15T14:30:00Z",
            "created_at": "2024-01-05T11:20:00Z",
            "updated_at": "2024-01-15T14:30:00Z",
            "segment_type": "activity",
            "criteria": {
              "last_active_days_min": 30,
              "status": ["active", "inactive"]
            }
          },
          {
            "id": "seg_003",
            "name": "New Users Dec 2023",
            "description": "Users registered in December 2023",
            "customer_count": 45200,
            "formatted_customer_count": "45,200",
            "last_refresh": "2024-01-14T09:00:00Z",
            "created_at": "2024-01-01T08:00:00Z",
            "updated_at": "2024-01-14T09:00:00Z",
            "segment_type": "demographic",
            "criteria": {
              "registration_date_from": "2023-12-01",
              "registration_date_to": "2023-12-31"
            }
          }
        ],
        "pagination": {
          "total": 4,
          "page": 1,
          "page_size": 10,
          "total_pages": 1
        },
        "summary": {
          "total_segments": 4,
          "total_customers_in_segments": 284200,
          "last_updated": "2024-01-15T14:30:00Z"
        }
      }
    },
    "create_segment": {
      "method": "POST",
      "endpoint": "/api/segments/create/",
      "description": "Create a new segment",
      "request": {
        "name": "High Value Addis Customers",
        "description": "Active users in Addis Ababa with high transaction volume",
        "config": {
          "autoRefresh": true,
          "refreshInterval": "daily",
          "ruleLogic": "AND",
          "status": "active"
        },
        "filters": {
          "behavioral": {
            "lastActivityDays": 30,
            "transactionCount": {
              "min": 10,
              "max": 100
            },
            "transactionValue": {
              "min": 5000,
              "max": 50000
            },
            "rewardReceived": "yes",
            "churnRisk": "low"
          },
          "demographic": {
            "region": "addis-ababa",
            "city": "addis",
            "gender": "female",
            "ageGroup": "25-34",
            "kycLevel": "verified",
            "deviceType": "smartphone"
          },
          "value": {
            "tier": "high"
          }
        }
      },
      "response": {
        "status": "success",
        "message": "Segment created successfully",
        "segment": {
          "id": "seg_20240115143045",
          "name": "High Value Addis Customers",
          "description": "Active users in Addis Ababa with high transaction volume",
          "segment_type": "behavioral",
          "customer_count": 125000,
          "formatted_customer_count": "125,000",
          "last_refresh": "2024-01-15T14:30:45Z",
          "created_at": "2024-01-15T14:30:45Z",
          "updated_at": "2024-01-15T14:30:45Z",
          "auto_refresh": true,
          "refresh_interval": "daily",
          "criteria": {
            "behavioral": {
              "lastActivityDays": 30,
              "transactionCount": {
                "min": 10,
                "max": 100
              },
              "transactionValue": {
                "min": 5000,
                "max": 50000
              },
              "rewardReceived": "yes",
              "churnRisk": "low"
            },
            "demographic": {
              "region": "addis-ababa",
              "city": "addis",
              "gender": "female",
              "ageGroup": "25-34",
              "kycLevel": "verified",
              "deviceType": "smartphone"
            },
            "value": {
              "tier": "high"
            },
            "rule_logic": "AND"
          },
          "metadata": {},
          "action": "view",
          "is_active": true
        },
        "estimated_preview": {
          "total_customers": 125000,
          "percent_of_base": 8.5,
          "active_rate": 78,
          "new_registrations": 12500,
          "high_value_percent": 35,
          "estimated_refresh_time": "5-10 minutes"
        }
      }
    },
    "segment_detail": {
      "method": "GET",
      "endpoint": "/api/segments/{id}/",
      "description": "Get detailed information for a specific segment",
      "response": {
        "status": "success",
        "segment": {
          "id": "seg_001",
          "name": "High Value Active Users",
          "description": "Active customers with high lifetime value",
          "segment_type": "behavioral",
          "customer_count": 125000,
          "formatted_customer_count": "125,000",
          "last_refresh": "2024-01-15T14:30:00Z",
          "created_at": "2024-01-10T09:15:00Z",
          "updated_at": "2024-01-15T14:30:00Z",
          "criteria": {
            "status": "active",
            "lifetime_value_min": 1000,
            "last_active_days_max": 30
          },
          "type": "Value",
          "last_refreshed": "2024-01-15 14:30",
          "new_users_30d": {
            "count": 4520,
            "percentage": 3.6
          },
          "value_distribution": {
            "high": 35,
            "medium": 45,
            "low": 20
          },
          "churn_risk": {
            "count": 8500,
            "avg_probability": 32
          },
          "customer_preview": [
            {
              "msisdn": "2547****123",
              "reg_date": "2023-06-15",
              "last_activity": "2024-01-14",
              "txn_count_30d": 45,
              "txn_value_30d": "KES 78,500",
              "value_tier": "High",
              "churn_risk": "Low"
            },
            {
              "msisdn": "2547****456",
              "reg_date": "2023-08-22",
              "last_activity": "2024-01-15",
              "txn_count_30d": 32,
              "txn_value_30d": "KES 52,000",
              "value_tier": "High",
              "churn_risk": "Low"
            },
            {
              "msisdn": "2547****789",
              "reg_date": "2023-03-10",
              "last_activity": "2024-01-10",
              "txn_count_30d": 18,
              "txn_value_30d": "KES 25,000",
              "value_tier": "Medium",
              "churn_risk": "Medium"
            },
            {
              "msisdn": "2547****101",
              "reg_date": "2023-07-05",
              "last_activity": "2024-01-13",
              "txn_count_30d": 28,
              "txn_value_30d": "KES 41,200",
              "value_tier": "Medium",
              "churn_risk": "Low"
            },
            {
              "msisdn": "2547****202",
              "reg_date": "2023-09-18",
              "last_activity": "2024-01-12",
              "txn_count_30d": 12,
              "txn_value_30d": "KES 18,900",
              "value_tier": "Low",
              "churn_risk": "High"
            },
            {
              "msisdn": "2547****303",
              "reg_date": "2023-05-22",
              "last_activity": "2024-01-11",
              "txn_count_30d": 55,
              "txn_value_30d": "KES 95,000",
              "value_tier": "High",
              "churn_risk": "Low"
            },
            {
              "msisdn": "2547****404",
              "reg_date": "2023-11-30",
              "last_activity": "2024-01-09",
              "txn_count_30d": 8,
              "txn_value_30d": "KES 12,500",
              "value_tier": "Low",
              "churn_risk": "High"
            },
            {
              "msisdn": "2547****505",
              "reg_date": "2023-04-14",
              "last_activity": "2024-01-08",
              "txn_count_30d": 41,
              "txn_value_30d": "KES 67,800",
              "value_tier": "High",
              "churn_risk": "Medium"
            },
            {
              "msisdn": "2547****606",
              "reg_date": "2023-10-08",
              "last_activity": "2024-01-07",
              "txn_count_30d": 22,
              "txn_value_30d": "KES 33,400",
              "value_tier": "Medium",
              "churn_risk": "Medium"
            },
            {
              "msisdn": "2547****707",
              "reg_date": "2023-12-01",
              "last_activity": "2024-01-06",
              "txn_count_30d": 15,
              "txn_value_30d": "KES 22,100",
              "value_tier": "Low",
              "churn_risk": "High"
            }
          ]
        }
      }
    },
    "update_segment": {
      "method": "PUT",
      "endpoint": "/api/segments/{id}/",
      "description": "Update a specific segment",
      "request": {
        "name": "High Value Active Users",
        "description": "Users with high transaction values",
        "config": {
          "autoRefresh": true,
          "refreshInterval": "daily",
          "ruleLogic": "AND"
        },
        "filters": {
          "behavioral": {
            "lastActivityDays": 30,
            "transactionCount": {
              "min": 10,
              "max": null
            },
            "transactionValue": {
              "min": 5000,
              "max": null
            },
            "rewardReceived": null,
            "churnRisk": null
          },
          "demographic": {
            "region": null,
            "city": null,
            "gender": null,
            "ageGroup": null,
            "kycLevel": null,
            "deviceType": null
          },
          "value": {
            "tier": "high"
          }
        }
      },
      "response": {
        "status": "success",
        "message": "Segment updated successfully",
        "segment": {
          "id": "seg_001",
          "name": "High Value Active Users",
          "description": "Users with high transaction values",
          "segment_type": "behavioral",
          "customer_count": 125000,
          "formatted_customer_count": "125,000",
          "last_refresh": "2024-01-15T14:30:00Z",
          "created_at": "2024-01-10T09:15:00Z",
          "updated_at": "2024-01-15T14:30:00Z",
          "auto_refresh": true,
          "refresh_interval": "daily",
          "criteria": {
            "behavioral": {
              "lastActivityDays": 30,
              "transactionCount": {
                "min": 10,
                "max": null
              },
              "transactionValue": {
                "min": 5000,
                "max": null
              },
              "rewardReceived": null,
              "churnRisk": null
            },
            "demographic": {
              "region": null,
              "city": null,
              "gender": null,
              "ageGroup": null,
              "kycLevel": null,
              "deviceType": null
            },
            "value": {
              "tier": "high"
            },
            "rule_logic": "AND"
          },
          "metadata": {},
          "action": "view",
          "is_active": true
        }
      }
    },
    "delete_segment": {
      "method": "DELETE",
      "endpoint": "/api/segments/{id}/delete/",
      "description": "Delete a specific segment",
      "response": {
        "status": "success",
        "message": "Segment deleted successfully"
      }
    }
  }
}
{
  "api_endpoints": {
    "list_reward_accounts": {
      "method": "GET",
      "endpoint": "/api/reward-accounts/",
      "description": "Get list of all reward accounts with pagination",
      "query_parameters": {
        "page": {
          "type": "integer",
          "default": 1,
          "description": "Page number for pagination"
        },
        "page_size": {
          "type": "integer",
          "default": 10,
          "description": "Number of items per page"
        }
      },
      "response": {
        "status": "success",
        "accounts": [
          {
            "id": 1,
            "account_id": "ACC_001",
            "account_name": "Marketing Budget 2024",
            "balance": 50000.00,
            "formatted_balance": "50,000.00 ETB",
            "currency": "ETB",
            "status": "active",
            "is_available": true,
            "assigned_campaigns_count": 3,
            "assigned_campaigns": [],
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
          }
        ],
        "pagination": {
          "total": 5,
          "page": 1,
          "page_size": 10,
          "total_pages": 1
        },
        "summary": {
          "total_accounts": 5,
          "active_accounts": 4,
          "total_balance": 250000.0,
          "formatted_total_balance": "250,000.00 ETB"
        }
      }
    },
    "create_reward_account": {
      "method": "POST",
      "endpoint": "/api/reward-accounts/create/",
      "description": "Create a new reward account",
      "request_body": {
        "account_id": "ACC_002",
        "account_name": "Holiday Campaign Fund",
        "balance": 25000.00,
        "currency": "ETB",
        "status": "active"
      },
      "response": {
        "status": "success",
        "message": "Reward account created successfully",
        "account": {
          "id": 2,
          "account_id": "ACC_002",
          "account_name": "Holiday Campaign Fund",
          "balance": 25000.00,
          "formatted_balance": "25,000.00 ETB",
          "currency": "ETB",
          "status": "active",
          "is_available": true,
          "assigned_campaigns_count": 0,
          "assigned_campaigns": [],
          "created_at": "2024-01-15T11:00:00Z",
          "updated_at": "2024-01-15T11:00:00Z"
        }
      }
    },
    "get_reward_account": {
      "method": "GET",
      "endpoint": "/api/reward-accounts/{account_id}/",
      "description": "Get details of a specific reward account",
      "path_parameters": {
        "account_id": {
          "type": "integer",
          "description": "ID of the reward account"
        }
      },
      "response": {
        "status": "success",
        "account": {
          "id": 1,
          "account_id": "ACC_001",
          "account_name": "Marketing Budget 2024",
          "balance": 50000.00,
          "formatted_balance": "50,000.00 ETB",
          "currency": "ETB",
          "status": "active",
          "is_available": true,
          "assigned_campaigns_count": 3,
          "assigned_campaigns": [],
          "created_at": "2024-01-15T10:30:00Z",
          "updated_at": "2024-01-15T10:30:00Z"
        }
      }
    },
    "update_reward_account": {
      "method": "PUT",
      "endpoint": "/api/reward-accounts/{account_id}/",
      "description": "Update a specific reward account",
      "path_parameters": {
        "account_id": {
          "type": "integer",
          "description": "ID of the reward account"
        }
      },
      "request_body": {
        "account_name": "Updated Marketing Budget 2024",
        "balance": 45000.00,
        "status": "active"
      },
      "response": {
        "status": "success",
        "message": "Reward account updated successfully",
        "account": {
          "id": 1,
          "account_id": "ACC_001",
          "account_name": "Updated Marketing Budget 2024",
          "balance": 45000.00,
          "formatted_balance": "45,000.00 ETB",
          "currency": "ETB",
          "status": "active",
          "is_available": true,
          "assigned_campaigns_count": 3,
          "assigned_campaigns": [],
          "created_at": "2024-01-15T10:30:00Z",
          "updated_at": "2024-01-15T12:00:00Z"
        }
      }
    },
    "delete_reward_account": {
      "method": "DELETE",
      "endpoint": "/api/reward-accounts/{account_id}/delete/",
      "description": "Delete a specific reward account",
      "path_parameters": {
        "account_id": {
          "type": "integer",
          "description": "ID of the reward account"
        }
      },
      "response": {
        "status": "success",
        "message": "Reward account deleted successfully"
      }
    }
  },
  "data_models": {
    "RewardAccount": {
      "id": "integer (auto-generated)",
      "account_id": "string (unique, max 100 chars)",
      "account_name": "string (max 255 chars)",
      "balance": "decimal (15 digits, 2 decimal places)",
      "formatted_balance": "string (computed field)",
      "currency": "string (max 3 chars, default 'ETB')",
      "status": "string (choices: active, inactive, frozen)",
      "is_available": "boolean (computed property)",
      "assigned_campaigns_count": "integer (computed field)",
      "assigned_campaigns": "array (ManyToManyField - commented out for now)",
      "created_at": "datetime (auto-generated)",
      "updated_at": "datetime (auto-generated)"
    },
    "RewardAccountStatus": {
      "ACTIVE": "'active' - Account is available for use",
      "INACTIVE": "'inactive' - Account is temporarily disabled",
      "FROZEN": "'frozen' - Account is frozen, no outgoing transactions"
    },
    "ValidationRules": {
      "balance": "Must be >= 0",
      "account_id": "Must be unique across all accounts",
      "currency": "ISO 4217 currency code (e.g., 'ETB', 'USD', 'EUR')"
    }
  },
  "business_logic": {
    "balance_validation": "Balance cannot be negative (enforced at model and serializer level)",
    "account_id_uniqueness": "Account ID must be unique across all reward accounts",
    "status_behavior": {
      "active": "Account can be used for campaigns and transactions",
      "inactive": "Account exists but cannot be used for new transactions",
      "frozen": "Account is locked, no outgoing transactions allowed"
    },
    "relationships": {
      "assigned_campaigns": "Many-to-many relationship with Campaign model (currently commented out)",
      "future_enhancements": "Will support campaign budget allocation and transaction tracking"
    }
  },
  "error_responses": {
    "validation_error": {
      "status": "error",
      "message": "Validation failed",
      "errors": {
        "account_id": ["Account ID must be unique."],
        "balance": ["Balance cannot be negative."]
      }
    },
    "not_found": {
      "status": "error",
      "message": "Reward account not found"
    },
    "permission_denied": {
      "status": "error",
      "message": "You do not have permission to perform this action"
    }
  }
}
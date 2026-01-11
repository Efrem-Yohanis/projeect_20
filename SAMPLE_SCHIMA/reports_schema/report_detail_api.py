# reports_schema/report_detail_api.py
"""
Report Detail API Schema

GET /api/reports/:id
Returns detailed information about a specific report including configuration and history
"""

# Request Schema (URL Parameter)
report_detail_request = {
    "type": "object",
    "properties": {
        "report_id": {
            "type": "string",
            "description": "Unique identifier for the report",
            "example": "rpt-001"
        }
    },
    "required": ["report_id"]
}

# Response Schema
report_detail_response = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "description": "Indicates if the request was successful"
        },
        "data": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Unique identifier for the report",
                    "example": "rpt-001"
                },
                "name": {
                    "type": "string",
                    "description": "Name of the report",
                    "example": "Q4 Revenue Analysis"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the report",
                    "example": "A detailed breakdown of revenue by region and product line for the final quarter."
                },
                "source_type": {
                    "type": "string",
                    "enum": ["campaign", "custom"],
                    "description": "Type of data source for the report"
                },
                "export_format": {
                    "type": "string",
                    "enum": ["pdf", "excel", "csv"],
                    "description": "Format in which the report should be exported"
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Timestamp when the report was created",
                    "example": "2024-01-10T10:00:00Z"
                },
                "configuration": {
                    "type": "object",
                    "description": "Detailed configuration for the report generation",
                    "properties": {
                        "custom_mode": {
                            "type": ["string", "null"],
                            "enum": ["filter", "sql", null],
                            "description": "Mode for custom reports (filter or sql)"
                        },
                        "campaign_id": {
                            "type": ["string", "null"],
                            "description": "ID of the campaign to base the report on (for campaign source_type)",
                            "example": "camp-123"
                        },
                        "sql_query": {
                            "type": ["string", "null"],
                            "description": "Custom SQL query for the report (for custom sql mode)",
                            "example": "SELECT region, SUM(revenue) as total_revenue FROM transactions WHERE date >= '2024-01-01' GROUP BY region ORDER BY total_revenue DESC"
                        },
                        "filters": {
                            "type": "array",
                            "description": "Array of filter conditions for custom filter mode",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "description": "Field name to filter on",
                                        "example": "transaction_value"
                                    },
                                    "operator": {
                                        "type": "string",
                                        "enum": ["equals", "greater_than", "less_than", "contains", "not_equals"],
                                        "description": "Comparison operator"
                                    },
                                    "value": {
                                        "type": "string",
                                        "description": "Value to compare against",
                                        "example": "1000"
                                    }
                                },
                                "required": ["field", "operator", "value"]
                            }
                        }
                    },
                    "required": ["custom_mode", "campaign_id", "sql_query", "filters"]
                },
                "scheduling": {
                    "type": "object",
                    "description": "Scheduling configuration for automated report generation",
                    "properties": {
                        "enabled": {
                            "type": "boolean",
                            "description": "Whether automated scheduling is enabled"
                        },
                        "frequency": {
                            "type": ["string", "null"],
                            "enum": ["daily", "weekly", "monthly", null],
                            "description": "How often the report should be generated"
                        },
                        "recipients": {
                            "type": "array",
                            "description": "List of email addresses to receive the report",
                            "items": {
                                "type": "string",
                                "format": "email",
                                "example": "finance-team@company.com"
                            }
                        }
                    },
                    "required": ["enabled", "frequency", "recipients"]
                },
                "history": {
                    "type": "array",
                    "description": "History of report generation attempts",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date and time of the generation attempt",
                                "example": "2024-01-15 09:00"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["Success", "Failed", "Pending"],
                                "description": "Status of the generation attempt"
                            },
                            "size": {
                                "type": ["string", "null"],
                                "description": "Size of the generated report file",
                                "example": "2.4 MB"
                            },
                            "duration": {
                                "type": ["string", "null"],
                                "description": "Time taken to generate the report",
                                "example": "45s"
                            },
                            "download_url": {
                                "type": ["string", "null"],
                                "description": "URL to download the generated report",
                                "example": "/api/reports/download/file-abc.pdf"
                            }
                        },
                        "required": ["date", "status", "size", "duration", "download_url"]
                    }
                }
            },
            "required": ["id", "name", "description", "source_type", "export_format", "created_at", "configuration", "scheduling", "history"]
        }
    },
    "required": ["success", "data"]
}

# Error Response Schema
report_detail_error_response = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": False
        },
        "message": {
            "type": "string",
            "description": "Error message",
            "example": "Report with ID rpt-999 not found"
        }
    },
    "required": ["success", "message"]
}

# Example Usage
if __name__ == "__main__":
    print("Report Detail API Schema")
    print("GET /api/reports/{report_id}")
    print("\nRequest: URL parameter 'report_id'")
    print("\nResponse: Detailed report information including configuration and history")
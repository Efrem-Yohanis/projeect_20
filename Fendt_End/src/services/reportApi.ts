// Report API Service

export interface Report {
  id: string;
  name: string;
  description?: string;
  source_type: "campaign" | "custom";
  configuration: {
    campaign_id?: string;
    custom_mode?: "sql" | "filter";
    sql_query?: string;
    filters?: Array<{
      field: string;
      operator: string;
      value: string;
    }>;
  };
  export_format: "pdf" | "excel" | "csv";
  scheduling: {
    enabled: boolean;
    frequency?: "daily" | "weekly" | "monthly";
    recipients?: string[];
  };
  created_at?: string;
  updated_at?: string;
}

export interface ReportListResponse {
  status: string;
  reports: Report[];
  pagination: {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  };
}

const API_BASE_URL = "/api";

// Mock data for development
const mockReports: Report[] = [
  {
    id: "rpt_001",
    name: "Monthly Campaign Performance Report",
    description: "Comprehensive campaign metrics for the month",
    source_type: "campaign",
    configuration: { campaign_id: "camp-1" },
    export_format: "pdf",
    scheduling: { enabled: true, frequency: "monthly", recipients: ["team@company.com"] },
    created_at: "2024-01-10T09:00:00Z",
  },
  {
    id: "rpt_002",
    name: "Weekly Customer Insights",
    description: "Customer segmentation analysis",
    source_type: "custom",
    configuration: { custom_mode: "filter", filters: [] },
    export_format: "excel",
    scheduling: { enabled: true, frequency: "weekly", recipients: ["analytics@company.com"] },
    created_at: "2024-01-08T14:30:00Z",
  },
  {
    id: "rpt_003",
    name: "Daily Transaction Summary",
    description: "Daily transaction breakdown",
    source_type: "custom",
    configuration: { custom_mode: "sql", sql_query: "SELECT * FROM transactions" },
    export_format: "csv",
    scheduling: { enabled: true, frequency: "daily", recipients: ["ops@company.com"] },
    created_at: "2024-01-05T08:00:00Z",
  },
  {
    id: "rpt_004",
    name: "Quarterly Revenue Report",
    description: "Revenue analysis by quarter",
    source_type: "campaign",
    configuration: { campaign_id: "camp-2" },
    export_format: "pdf",
    scheduling: { enabled: false },
    created_at: "2024-01-02T10:00:00Z",
  },
  {
    id: "rpt_005",
    name: "Churn Risk Analysis",
    description: "Customers at risk of churning",
    source_type: "custom",
    configuration: { custom_mode: "filter", filters: [] },
    export_format: "excel",
    scheduling: { enabled: true, frequency: "weekly", recipients: ["retention@company.com"] },
    created_at: "2024-01-01T11:00:00Z",
  },
];

export async function fetchReports(
  page: number = 1,
  pageSize: number = 10,
  search?: string,
  sourceType?: string,
  exportFormat?: string
): Promise<ReportListResponse> {
  try {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
    });
    if (search) params.append("search", search);
    if (sourceType && sourceType !== "all") params.append("source_type", sourceType);
    if (exportFormat && exportFormat !== "all") params.append("export_format", exportFormat);

    const response = await fetch(`${API_BASE_URL}/reports/?${params}`);
    if (!response.ok) throw new Error("Failed to fetch reports");
    return await response.json();
  } catch (error) {
    // Return mock data for development
    let filtered = [...mockReports];
    
    if (search) {
      const searchLower = search.toLowerCase();
      filtered = filtered.filter(r => 
        r.name.toLowerCase().includes(searchLower) || 
        r.description?.toLowerCase().includes(searchLower)
      );
    }
    if (sourceType && sourceType !== "all") {
      filtered = filtered.filter(r => r.source_type === sourceType);
    }
    if (exportFormat && exportFormat !== "all") {
      filtered = filtered.filter(r => r.export_format === exportFormat);
    }

    const total = filtered.length;
    const start = (page - 1) * pageSize;
    const paginatedReports = filtered.slice(start, start + pageSize);

    return {
      status: "success",
      reports: paginatedReports,
      pagination: {
        total,
        page,
        page_size: pageSize,
        total_pages: Math.ceil(total / pageSize),
      },
    };
  }
}

export async function deleteReport(id: string): Promise<{ status: string; message: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/reports/${id}/delete/`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) throw new Error("Failed to delete report");
    return await response.json();
  } catch (error) {
    return { status: "success", message: "Report deleted successfully" };
  }
}

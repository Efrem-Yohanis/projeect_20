import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Save, X } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { useReports } from "@/hooks/useReports";
import { toast } from "sonner";

export default function ReportEdit() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { data } = useReports(1, 100);

  // Find the report by ID
  const report = data?.reports?.find(r => r.id === id);

  // Form state
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    source_type: "campaign",
    export_format: "pdf",
    campaign_id: "",
    custom_mode: "filter",
    sql_query: "",
    scheduling_enabled: false,
    scheduling_frequency: "daily",
    recipients: "",
  });

  // Load report data into form
  useEffect(() => {
    if (report) {
      setFormData({
        name: report.name || "",
        description: report.description || "",
        source_type: report.source_type || "campaign",
        export_format: report.export_format || "pdf",
        campaign_id: report.configuration?.campaign_id || "",
        custom_mode: report.configuration?.custom_mode || "filter",
        sql_query: report.configuration?.sql_query || "",
        scheduling_enabled: report.scheduling?.enabled || false,
        scheduling_frequency: report.scheduling?.frequency || "daily",
        recipients: report.scheduling?.recipients?.join(", ") || "",
      });
    }
  }, [report]);

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    if (!formData.name.trim()) {
      toast.error("Report name is required");
      return;
    }
    // In a real app, this would call an API to save
    toast.success("Report updated successfully");
    navigate(`/reports/${id}`);
  };

  const handleCancel = () => {
    navigate(`/reports/${id}`);
  };

  if (!report) {
    return (
      <div className="space-y-6 animate-fade-in">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate("/reports")} className="rounded-none">
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold">Report Not Found</h1>
            <p className="text-muted-foreground">The requested report could not be found.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={handleCancel} className="rounded-none">
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold">Edit Report</h1>
            <p className="text-muted-foreground">Modify report configuration and settings</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="gap-2 rounded-none" onClick={handleCancel}>
            <X className="w-4 h-4" />
            Cancel
          </Button>
          <Button className="gap-2 rounded-none" onClick={handleSave}>
            <Save className="w-4 h-4" />
            Save Changes
          </Button>
        </div>
      </div>

      {/* Basic Information */}
      <Card className="rounded-none">
        <CardHeader>
          <CardTitle className="text-lg">Basic Information</CardTitle>
          <CardDescription>Report name and description</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Report Name *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange("name", e.target.value)}
                placeholder="Enter report name"
                className="rounded-none"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="export_format">Export Format</Label>
              <Select
                value={formData.export_format}
                onValueChange={(value) => handleInputChange("export_format", value)}
              >
                <SelectTrigger className="rounded-none">
                  <SelectValue placeholder="Select format" />
                </SelectTrigger>
                <SelectContent className="rounded-none">
                  <SelectItem value="pdf">PDF</SelectItem>
                  <SelectItem value="excel">Excel</SelectItem>
                  <SelectItem value="csv">CSV</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => handleInputChange("description", e.target.value)}
              placeholder="Enter report description"
              className="rounded-none min-h-[100px]"
            />
          </div>
        </CardContent>
      </Card>

      {/* Data Source Configuration */}
      <Card className="rounded-none">
        <CardHeader>
          <CardTitle className="text-lg">Data Source Configuration</CardTitle>
          <CardDescription>Configure the data source for this report</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="source_type">Source Type</Label>
            <Select
              value={formData.source_type}
              onValueChange={(value) => handleInputChange("source_type", value)}
            >
              <SelectTrigger className="rounded-none">
                <SelectValue placeholder="Select source type" />
              </SelectTrigger>
              <SelectContent className="rounded-none">
                <SelectItem value="campaign">Campaign</SelectItem>
                <SelectItem value="custom">Custom</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {formData.source_type === "campaign" && (
            <div className="space-y-2">
              <Label htmlFor="campaign_id">Campaign ID</Label>
              <Input
                id="campaign_id"
                value={formData.campaign_id}
                onChange={(e) => handleInputChange("campaign_id", e.target.value)}
                placeholder="Enter campaign ID"
                className="rounded-none"
              />
            </div>
          )}

          {formData.source_type === "custom" && (
            <>
              <div className="space-y-2">
                <Label htmlFor="custom_mode">Custom Mode</Label>
                <Select
                  value={formData.custom_mode}
                  onValueChange={(value) => handleInputChange("custom_mode", value)}
                >
                  <SelectTrigger className="rounded-none">
                    <SelectValue placeholder="Select mode" />
                  </SelectTrigger>
                  <SelectContent className="rounded-none">
                    <SelectItem value="filter">Filter Builder</SelectItem>
                    <SelectItem value="sql">SQL Query</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {formData.custom_mode === "sql" && (
                <div className="space-y-2">
                  <Label htmlFor="sql_query">SQL Query</Label>
                  <Textarea
                    id="sql_query"
                    value={formData.sql_query}
                    onChange={(e) => handleInputChange("sql_query", e.target.value)}
                    placeholder="Enter SQL query"
                    className="rounded-none min-h-[150px] font-mono text-sm"
                  />
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* Scheduling Configuration */}
      <Card className="rounded-none">
        <CardHeader>
          <CardTitle className="text-lg">Scheduling</CardTitle>
          <CardDescription>Configure automated report generation</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-muted/30 border">
            <div>
              <p className="font-medium">Enable Scheduling</p>
              <p className="text-sm text-muted-foreground">Automatically generate reports on a schedule</p>
            </div>
            <Switch
              checked={formData.scheduling_enabled}
              onCheckedChange={(checked) => handleInputChange("scheduling_enabled", checked)}
            />
          </div>

          {formData.scheduling_enabled && (
            <>
              <Separator />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="scheduling_frequency">Frequency</Label>
                  <Select
                    value={formData.scheduling_frequency}
                    onValueChange={(value) => handleInputChange("scheduling_frequency", value)}
                  >
                    <SelectTrigger className="rounded-none">
                      <SelectValue placeholder="Select frequency" />
                    </SelectTrigger>
                    <SelectContent className="rounded-none">
                      <SelectItem value="daily">Daily</SelectItem>
                      <SelectItem value="weekly">Weekly</SelectItem>
                      <SelectItem value="monthly">Monthly</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="recipients">Recipients (comma-separated)</Label>
                  <Input
                    id="recipients"
                    value={formData.recipients}
                    onChange={(e) => handleInputChange("recipients", e.target.value)}
                    placeholder="email1@example.com, email2@example.com"
                    className="rounded-none"
                  />
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Action Buttons (Bottom) */}
      <div className="flex items-center justify-end gap-2 pt-4">
        <Button variant="outline" className="gap-2 rounded-none" onClick={handleCancel}>
          <X className="w-4 h-4" />
          Cancel
        </Button>
        <Button className="gap-2 rounded-none" onClick={handleSave}>
          <Save className="w-4 h-4" />
          Save Changes
        </Button>
      </div>
    </div>
  );
}

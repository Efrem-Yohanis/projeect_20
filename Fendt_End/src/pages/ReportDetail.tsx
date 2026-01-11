import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, FileText, Clock, Mail, Calendar, Play, Database, Filter, Code, Pencil, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { useReports } from "@/hooks/useReports";

export default function ReportDetail() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { data } = useReports(1, 100);

  // Find the report by ID
  const report = data?.reports?.find(r => r.id === id);

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

  const getFormatBadge = (format: string) => {
    const variants: Record<string, "default" | "secondary" | "outline"> = {
      pdf: "default",
      excel: "secondary",
      csv: "outline",
    };
    return (
      <Badge variant={variants[format] || "secondary"} className="uppercase">
        {format}
      </Badge>
    );
  };

  const getSourceTypeBadge = (sourceType: string) => {
    return (
      <Badge variant={sourceType === "campaign" ? "default" : "outline"} className="capitalize">
        {sourceType}
      </Badge>
    );
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate("/reports")} className="rounded-none">
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{report.name}</h1>
            <p className="text-muted-foreground">{report.description || "No description provided"}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="gap-2 rounded-none" onClick={() => navigate(`/reports/${id}/edit`)}>
            <Pencil className="w-4 h-4" />
            Edit Report
          </Button>
          <Button className="gap-2 rounded-none">
            <Play className="w-4 h-4" />
            Run Now
          </Button>
        </div>
      </div>

      {/* Report Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="rounded-none">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-primary/10">
                {report.source_type === "campaign" ? (
                  <Play className="w-6 h-6 text-primary" />
                ) : (
                  <Database className="w-6 h-6 text-primary" />
                )}
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Source Type</p>
                <p className="font-semibold capitalize">{report.source_type}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-none">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-info/10">
                <FileText className="w-6 h-6 text-info" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Export Format</p>
                <p className="font-semibold uppercase">{report.export_format}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-none">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-success/10">
                <Clock className="w-6 h-6 text-success" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Schedule</p>
                <p className="font-semibold">
                  {report.scheduling?.enabled ? report.scheduling.frequency : "Manual"}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-none">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-warning/10">
                <Calendar className="w-6 h-6 text-warning" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Created</p>
                <p className="font-semibold">
                  {report.created_at ? new Date(report.created_at).toLocaleDateString() : "N/A"}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Configuration Details */}
        <Card className="rounded-none">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              {report.source_type === "campaign" ? (
                <Play className="w-5 h-5" />
              ) : report.configuration?.custom_mode === "sql" ? (
                <Code className="w-5 h-5" />
              ) : (
                <Filter className="w-5 h-5" />
              )}
              Configuration
            </CardTitle>
            <CardDescription>Report data source configuration</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {report.source_type === "campaign" && (
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-muted/50 border">
                  <span className="text-muted-foreground">Campaign ID</span>
                  <span className="font-medium">{report.configuration?.campaign_id || "N/A"}</span>
                </div>
              </div>
            )}

            {report.source_type === "custom" && report.configuration?.custom_mode === "sql" && (
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-muted-foreground mb-2">SQL Query</p>
                  <pre className="p-3 bg-muted/50 border text-sm font-mono overflow-x-auto">
                    {report.configuration.sql_query || "No query defined"}
                  </pre>
                </div>
              </div>
            )}

            {report.source_type === "custom" && report.configuration?.custom_mode === "filter" && (
              <div className="space-y-3">
                <p className="text-sm text-muted-foreground">Filter Criteria</p>
                {report.configuration?.filters && report.configuration.filters.length > 0 ? (
                  <div className="space-y-2">
                    {report.configuration.filters.map((filter, idx) => (
                      <div key={idx} className="flex items-center gap-2 p-3 bg-muted/50 border">
                        <Badge variant="outline">{filter.field}</Badge>
                        <span className="text-muted-foreground">{filter.operator}</span>
                        <Badge variant="secondary">{filter.value}</Badge>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No filters configured</p>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Scheduling Details */}
        <Card className="rounded-none">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Clock className="w-5 h-5" />
              Scheduling
            </CardTitle>
            <CardDescription>Automated report generation settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-muted/50 border">
              <span className="text-muted-foreground">Status</span>
              <Badge variant={report.scheduling?.enabled ? "default" : "secondary"}>
                {report.scheduling?.enabled ? "Enabled" : "Disabled"}
              </Badge>
            </div>

            {report.scheduling?.enabled && (
              <>
                <div className="flex justify-between items-center p-3 bg-muted/50 border">
                  <span className="text-muted-foreground">Frequency</span>
                  <span className="font-medium capitalize">{report.scheduling.frequency}</span>
                </div>

                {report.scheduling.recipients && report.scheduling.recipients.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground flex items-center gap-2">
                      <Mail className="w-4 h-4" />
                      Recipients
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {report.scheduling.recipients.map((email, idx) => (
                        <Badge key={idx} variant="outline">
                          {email}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {!report.scheduling?.enabled && (
              <p className="text-sm text-muted-foreground">
                This report is generated manually. Enable scheduling to automate report generation.
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Report History */}
      <Card className="rounded-none">
        <CardHeader>
          <CardTitle className="text-lg">Generation History</CardTitle>
          <CardDescription>Recent report generation runs</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { date: "2024-01-15 09:00", status: "Success", size: "2.4 MB", duration: "45s" },
              { date: "2024-01-08 09:00", status: "Success", size: "2.1 MB", duration: "42s" },
              { date: "2024-01-01 09:00", status: "Success", size: "1.9 MB", duration: "38s" },
            ].map((run, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-muted/30 border hover:bg-muted/50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="p-2 rounded-lg bg-accent">
                    <FileText className="w-4 h-4 text-accent-foreground" />
                  </div>
                  <div>
                    <p className="font-medium">{run.date}</p>
                    <p className="text-sm text-muted-foreground">Duration: {run.duration}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <Badge variant="outline" className="bg-success/10 text-success border-success/20">
                    {run.status}
                  </Badge>
                  <span className="text-sm text-muted-foreground">{run.size}</span>
                  <Button variant="ghost" size="icon">
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

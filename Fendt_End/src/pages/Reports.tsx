import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileText, Search, Eye, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { useReports } from "@/hooks/useReports";
import type { Report } from "@/services/reportApi";

export default function Reports() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [sourceTypeFilter, setSourceTypeFilter] = useState("all");
  const [formatFilter, setFormatFilter] = useState("all");
  const pageSize = 10;

  const { data, isLoading } = useReports(page, pageSize, debouncedSearch, sourceTypeFilter, formatFilter);

  const handleSearch = (value: string) => {
    setSearchQuery(value);
    // Simple debounce
    setTimeout(() => {
      setDebouncedSearch(value);
      setPage(1);
    }, 300);
  };

  const handleFilterChange = (type: "source" | "format", value: string) => {
    if (type === "source") {
      setSourceTypeFilter(value);
    } else {
      setFormatFilter(value);
    }
    setPage(1);
  };

  const getSchedulingDisplay = (report: Report) => {
    if (!report.scheduling?.enabled) {
      return <Badge variant="secondary">Manual</Badge>;
    }
    return (
      <div className="flex items-center gap-2">
        <Badge variant="outline" className="capitalize">
          <Clock className="w-3 h-3 mr-1" />
          {report.scheduling.frequency}
        </Badge>
      </div>
    );
  };

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
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Reports</h1>
          <p className="text-muted-foreground">View and manage all generated reports</p>
        </div>
        <Button className="gap-2" onClick={() => navigate("/reports/create")}>
          <FileText className="w-4 h-4" />
          Create Report
        </Button>
      </div>

      {/* Filters Section */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Search & Filter</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                placeholder="Search reports by name..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={sourceTypeFilter} onValueChange={(v) => handleFilterChange("source", v)}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Source Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Sources</SelectItem>
                <SelectItem value="campaign">Campaign</SelectItem>
                <SelectItem value="custom">Custom</SelectItem>
              </SelectContent>
            </Select>
            <Select value={formatFilter} onValueChange={(v) => handleFilterChange("format", v)}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Format" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Formats</SelectItem>
                <SelectItem value="pdf">PDF</SelectItem>
                <SelectItem value="excel">Excel</SelectItem>
                <SelectItem value="csv">CSV</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Reports Table */}
      <Card>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Source Type</TableHead>
                    <TableHead>Scheduling</TableHead>
                    <TableHead>Export Format</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data?.reports && data.reports.length > 0 ? (
                    data.reports.map((report) => (
                      <TableRow key={report.id}>
                        <TableCell>
                          <div>
                            <p className="font-medium">{report.name}</p>
                            {report.description && (
                              <p className="text-sm text-muted-foreground truncate max-w-xs">
                                {report.description}
                              </p>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>{getSourceTypeBadge(report.source_type)}</TableCell>
                        <TableCell>{getSchedulingDisplay(report)}</TableCell>
                        <TableCell>{getFormatBadge(report.export_format)}</TableCell>
                        <TableCell>
                          <div className="flex items-center justify-end">
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              title="View"
                              onClick={() => navigate(`/reports/${report.id}`)}
                            >
                              <Eye className="w-4 h-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                        No reports found
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>

              {/* Pagination */}
              {data?.pagination && data.pagination.total_pages > 1 && (
                <div className="flex items-center justify-between px-4 py-4 border-t">
                  <p className="text-sm text-muted-foreground">
                    Showing {((page - 1) * pageSize) + 1} to {Math.min(page * pageSize, data.pagination.total)} of {data.pagination.total} reports
                  </p>
                  <Pagination>
                    <PaginationContent>
                      <PaginationItem>
                        <PaginationPrevious
                          onClick={() => setPage((p) => Math.max(1, p - 1))}
                          className={page === 1 ? "pointer-events-none opacity-50" : "cursor-pointer"}
                        />
                      </PaginationItem>
                      {Array.from({ length: data.pagination.total_pages }, (_, i) => i + 1).map((pageNum) => (
                        <PaginationItem key={pageNum}>
                          <PaginationLink
                            onClick={() => setPage(pageNum)}
                            isActive={page === pageNum}
                            className="cursor-pointer"
                          >
                            {pageNum}
                          </PaginationLink>
                        </PaginationItem>
                      ))}
                      <PaginationItem>
                        <PaginationNext
                          onClick={() => setPage((p) => Math.min(data.pagination.total_pages, p + 1))}
                          className={page === data.pagination.total_pages ? "pointer-events-none opacity-50" : "cursor-pointer"}
                        />
                      </PaginationItem>
                    </PaginationContent>
                  </Pagination>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchReports, deleteReport } from "@/services/reportApi";
import { toast } from "@/hooks/use-toast";

export function useReports(
  page: number = 1,
  pageSize: number = 10,
  search?: string,
  sourceType?: string,
  exportFormat?: string
) {
  return useQuery({
    queryKey: ["reports", page, pageSize, search, sourceType, exportFormat],
    queryFn: () => fetchReports(page, pageSize, search, sourceType, exportFormat),
  });
}

export function useDeleteReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => deleteReport(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reports"] });
      toast({
        title: "Report Deleted",
        description: "The report has been deleted successfully.",
      });
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to delete the report.",
        variant: "destructive",
      });
    },
  });
}

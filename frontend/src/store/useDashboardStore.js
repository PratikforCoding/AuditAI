import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useDashboardStore = create((set, get) => ({
    summaryData: null,
    recentAudits: [],

    isDashboardLoading: false,

    fetchDashboardData: async () => {
        try {
            set({ isDashboardLoading: true });

            // Fetching in parallel
            const [costRes, recRes] = await Promise.all([
                axiosInstance.get("/cost-analysis"),
                axiosInstance.get("/recommendations-summary")
            ]);

            set({
                summaryData: {
                    ...recRes.data.data, // assuming struct
                    costAnalysis: costRes.data.data
                },
                // Assuming recent audits might come from one of these or a separate endpoint not fully specified, 
                // but we can map what we have. 
                // For now, let's store what we got.
            });

            return { cost: costRes.data, rec: recRes.data };
        } catch (error) {
            console.error("Error fetching dashboard data:", error);
        } finally {
            set({ isDashboardLoading: false });
        }
    },
}));

export default useDashboardStore;

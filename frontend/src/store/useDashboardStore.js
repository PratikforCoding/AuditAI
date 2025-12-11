import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useDashboardStore = create((set, get) => ({
    summaryData: null,
    recentAudits: [],

    isDashboardLoading: false,

    fetchDashboardData: async () => {
        try {
            set({ isDashboardLoading: true });
        } catch (error) {
        } finally {
            set({ isDashboardLoading: false });
        }
    },
}));

export default useDashboardStore;

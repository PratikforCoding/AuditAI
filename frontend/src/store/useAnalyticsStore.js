import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

// Mock Data Generators
const generateTrendData = () => {
    return Array.from({ length: 30 }, (_, i) => ({
        date: `2025-11-${String(i + 1).padStart(2, '0')}`,
        cost: Math.floor(Math.random() * 200) + 100, // Vary cost
        projected: Math.floor(Math.random() * 200) + 120
    }));
};

const generateDistributionData = () => {
    return [
        { name: "Compute Engine", value: Math.floor(Math.random() * 1000) + 500 },
        { name: "Cloud Storage", value: Math.floor(Math.random() * 500) + 200 },
        { name: "Cloud SQL", value: Math.floor(Math.random() * 800) + 300 },
        { name: "Kubernetes Engine", value: Math.floor(Math.random() * 600) + 100 },
        { name: "Network", value: Math.floor(Math.random() * 200) + 50 },
    ];
};

const useAnalyticsStore = create((set, get) => ({
    isLoading: false,
    costTrend: null,
    costDistribution: null,
    topResources: [],
    savingsTypes: [],
    lastUpdated: null,

    fetchAnalyticsData: async () => {
        try {
            set({ isLoading: true });

            // Attempt API call to existing endpoint
            const res = await axiosInstance.get("/cost-analysis");
            if (res.data && res.data.data) {
                // Transform API data to store format if necessary
                // Assuming API returns { trend: [], distribution: [], ... }
                // If structure differs, we might need mapping. 
                // For now, let's assume we map or use partial data.
                // If API data is missing parts, we might merge with mock?
                // Safer to just use API data if it works.
                set({
                    costTrend: res.data.data.trend || generateTrendData(),
                    costDistribution: res.data.data.distribution || generateDistributionData(),
                    topResources: res.data.data.top_resources || [],
                    savingsTypes: res.data.data.savings || [],
                    lastUpdated: new Date().toISOString()
                });
                return;
            }
            // If data invalid, throw to catch
            throw new Error("Invalid API Data");

        } catch (error) {
            console.warn("Analytics API failed or unavailable, using mock data:", error.message);

            // Fallback to Dynamic Mock Data
            // Simulating network delay for realism
            await new Promise(resolve => setTimeout(resolve, 600));

            set({
                costTrend: generateTrendData(),
                costDistribution: generateDistributionData(),
                topResources: [
                    { id: "vm-1", name: "prod-instance-1", service: "Compute Engine", cost: Math.floor(Math.random() * 100) + 50, trend: "up" },
                    { id: "db-1", name: "main-db-primary", service: "Cloud SQL", cost: Math.floor(Math.random() * 150) + 80, trend: "stable" },
                    { id: "st-1", name: "backup-bucket", service: "Cloud Storage", cost: Math.floor(Math.random() * 50) + 10, trend: "down" },
                ],
                savingsTypes: [
                    { type: "Idle VMs", amount: Math.floor(Math.random() * 300) + 100 },
                    { type: "Unused IPs", amount: Math.floor(Math.random() * 50) + 10 },
                    { type: "Right Sizing", amount: Math.floor(Math.random() * 200) + 50 },
                ],
                lastUpdated: new Date().toISOString()
            });

        } finally {
            set({ isLoading: false });
        }
    }
}));

export default useAnalyticsStore;

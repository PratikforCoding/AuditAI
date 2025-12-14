import { create } from "zustand";

const mockRecs = [
    {
        id: "rec_1",
        title: "Delete unused-vm-3",
        type: "Compute",
        savings: 150,
        risk: "Low",
        difficulty: "Easy",
        daysIdle: 45,
        description: "VM idle for 45 days. Consistently low CPU.",
    },
    {
        id: "rec_2",
        title: "Resize prod-db 16→8GB RAM",
        type: "Database",
        savings: 320,
        risk: "Medium",
        difficulty: "Medium",
        usage: "25%",
        description: "Memory utilization peaks at 25%. Downsizing recommended.",
    },
    {
        id: "rec_3",
        title: "Archive old-storage bucket",
        type: "Storage",
        savings: 80,
        risk: "Low",
        difficulty: "Easy",
        size: "500GB",
        description: "No read/write operations in last 90 days.",
    }
];

import axiosInstance from "@/utils/axiosInstance";

const useRecommendationStore = create((set) => ({
    recommendations: [],
    appliedItems: [],
    isLoading: false,

    fetchRecommendations: async () => {
        try {
            set({ isLoading: true });

            // Attempt Real API
            // Note: API might return summary, not list. We might need a list endpoint.
            // If /recommendations-summary returns list, good. If not, we might need /recommendations
            // Let's try /recommendations first as it's more standard for a list.
            const res = await axiosInstance.get("/recommendations");
            if (res.data && Array.isArray(res.data.data)) {
                set({ recommendations: res.data.data });
                return;
            } else {
                // Try summary if list failed or empty?
                // Or just throw to fallback
                throw new Error("API did not return recommendations list");
            }

        } catch (error) {
            console.warn("Recommendations API failed, using mock data:", error.message);
            // Fallback to Mock
            await new Promise(r => setTimeout(r, 600));
            // Randomize mock data slightly
            const recs = mockRecs.map(r => ({ ...r, savings: r.savings + Math.floor(Math.random() * 20 - 10) }));
            set({ recommendations: recs });
        } finally {
            set({ isLoading: false });
        }
    },

    applyRecommendation: (id) => {
        set(state => {
            const item = state.recommendations.find(r => r.id === id);
            if (!item) return state;
            const newItem = {
                ...item,
                appliedDate: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
            };
            return {
                recommendations: state.recommendations.filter(r => r.id !== id),
                appliedItems: [newItem, ...state.appliedItems]
            };
        });
    }
}));

export default useRecommendationStore;

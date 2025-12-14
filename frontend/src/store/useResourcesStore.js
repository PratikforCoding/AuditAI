import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useResourcesStore = create((set, get) => ({
    //array of resource objects [{},{},{}]
    resources: [],
    isResourcesLoading: false,

    fetchResources: async () => {
        try {
            set({ isResourcesLoading: true });
            const res = await axiosInstance.get("/resources");
            if (res.data && Array.isArray(res.data.data)) {
                set({ resources: res.data.data });
                return;
            }
            throw new Error("Invalid resource data");
        } catch (error) {
            console.warn("Resources API failed, using mock:", error.message);
            // Mock Data Generation
            await new Promise(r => setTimeout(r, 1000));
            const types = ["Compute", "Storage", "Database", "Network"];
            const statuses = ["Running", "Idle", "Stopped", "Error"];
            const zones = ["us-east-1a", "us-east-1b", "us-west-2a", "eu-central-1"];

            const mockResources = Array.from({ length: 45 }, (_, i) => ({
                id: `res-${i + 1}`,
                name: `${types[i % 4].toLowerCase()}-instance-${i + 100}`,
                type: types[i % 4],
                status: statuses[Math.floor(Math.random() * statuses.length)],
                zone: zones[Math.floor(Math.random() * zones.length)],
                cpu_utilization: Math.floor(Math.random() * 90),
                cost: Math.floor(Math.random() * 500) + 20,
                last_active: new Date().toISOString()
            }));
            set({ resources: mockResources });
        } finally {
            set({ isResourcesLoading: false });
        }
    },
}));

export default useResourcesStore;

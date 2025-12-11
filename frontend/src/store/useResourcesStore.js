import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useResourcesStore = create((set, get) => ({
    //array of resource objects [{},{},{}]
    resources: [],
    isResourcesLoading: false,

    fetchResources: async () => {
        try {
            set({ isResourcesLoading: true });
        } catch (error) {
        } finally {
            set({ isResourcesLoading: false });
        }
    },
}));

export default useResourcesStore;

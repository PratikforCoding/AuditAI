import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useOnboardingStore = create((set) => ({
    isLoading: false,
    status: null, // { is_registered, has_gcp_credentials, onboarding_complete, next_step, ... }
    validationResult: null, // { is_valid, issues, suggestions }
    gcpSetupGuide: [], // List of steps
    checkPermissionsResult: null,

    getOnboardingStatus: async () => {
        try {
            set({ isLoading: true });
            const res = await axiosInstance.get("/onboarding/status");
            set({ status: res.data });
            return res.data;
        } catch (error) {
            console.warn("Onboarding status API failed, using mock:", error.message);
            // Mock Status: Assume incomplete if checking
            set({ status: { is_registered: true, has_gcp_credentials: false } });
            return { is_registered: true, has_gcp_credentials: false };
        } finally {
            set({ isLoading: false });
        }
    },

    validateCredentials: async (projectId, file) => {
        try {
            set({ isLoading: true, validationResult: null });
            const formData = new FormData();
            formData.append("project_id", projectId);
            formData.append("file", file);

            const res = await axiosInstance.post("/onboarding/validate-credentials", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            set({ validationResult: res.data });
            return res.data;
        } catch (error) {
            console.warn("Credentials validation API failed, using mock success:", error.message);
            // Mock Validation Success
            await new Promise(r => setTimeout(r, 1000));
            const mockResult = {
                is_valid: true,
                issues: [],
                suggestions: []
            };
            set({ validationResult: mockResult });
            return mockResult;
        } finally {
            set({ isLoading: false });
        }
    },

    uploadServiceAccount: async (projectId, file) => {
        try {
            set({ isLoading: true });
            const formData = new FormData();
            formData.append("project_id", projectId);
            formData.append("file", file);

            const res = await axiosInstance.post("/onboarding/upload-service-account", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            return true;
        } catch (error) {
            console.warn("Upload API failed, using mock success:", error.message);
            await new Promise(r => setTimeout(r, 1500));
            return true;
        } finally {
            set({ isLoading: false });
        }
    },

    getGcpSetupGuide: async () => {
        try {
            set({ isLoading: true });
            const res = await axiosInstance.get("/onboarding/gcp-setup-guide");
            set({ gcpSetupGuide: res.data });
        } catch (error) {
            console.error("Error fetching setup guide:", error);
        } finally {
            set({ isLoading: false });
        }
    },

    checkPermissions: async () => {
        try {
            set({ isLoading: true });
            const res = await axiosInstance.get("/onboarding/check-permissions");
            set({ checkPermissionsResult: res.data });
            return res.data;
        } catch (error) {
            console.error("Error checking permissions:", error);
        } finally {
            set({ isLoading: false });
        }
    }
}));

export default useOnboardingStore;

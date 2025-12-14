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
            console.error("Error fetching onboarding status:", error);
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
            console.error("Error validating credentials:", error);
            // return structure to handle UI error
            return { is_valid: false, issues: ["Network or server error"] };
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
            // Update status immediately or assume success
            return true;
        } catch (error) {
            console.error("Error uploading service account:", error);
            return false;
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

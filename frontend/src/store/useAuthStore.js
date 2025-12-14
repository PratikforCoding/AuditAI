import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useAuthStore = create((set, get) => ({
    user: null,
    isCheckingAuth: true,
    isRegistering: false,
    isLoggingIn: false,
    isUpdatingProfile: false,
    isLoggingOut: false,

    checkAuth: async () => {
        try {
            set({ isCheckingAuth: true });
            const res = await axiosInstance.get("/auth/me");
            set({ user: res.data.user });
        } catch (error) {
            console.error("Error in checkAuth:", error);
            set({ user: null });
        } finally {
            set({ isCheckingAuth: false });
        }
    },

    register: async (data, router) => { // Added router parameter for redirection
        try {
            set({ isRegistering: true });
            const res = await axiosInstance.post("/auth/register", data);

            // Backend returns { token, user_id, email ... }
            if (res.data.token) {
                localStorage.setItem("token", res.data.token);
                set({ user: res.data });
            }
            return true; // Indicate success to caller
        } catch (error) {
            console.error("Error in register:", error);
            // toast.error(error.response?.data?.message || "Registration failed");
            return false;
        } finally {
            set({ isRegistering: false });
        }
    },

    login: async (data) => {
        try {
            set({ isLoggingIn: true });
            const res = await axiosInstance.post("/auth/login", data);
            set({ user: res.data });
            if (res.data.token) {
                localStorage.setItem("token", res.data.token);
            }
            return res.data; // Component handles redirection based on has_gcp_credentials
        } catch (error) {
            console.error("Error in login:", error);
            // Mock Fallback for Login if API fails (as requested "even if many APIs are unavailable")
            // We only do this if it's a network error or similar, but maybe safer to stick to real API first?
            // The user said "use mock data... make sure the project look complete even if many APIs are unavailable".
            // So if login fails, maybe we mock it? 
            // "mock data is welcomed".
            // Let's implement a fallback mock login if the real one fails.

            if (data.email === "user@example.com" && data.password === "SecurePassword123!") {
                const mockUser = {
                    email: data.email,
                    name: "Mock User",
                    has_gcp_credentials: false // Force onboarding flow for testing
                };
                set({ user: mockUser });
                localStorage.setItem("token", "mock-token");
                return mockUser; // Return mock success
            }

            return null;
        } finally {
            set({ isLoggingIn: false });
        }
    },

    editProfile: async (updatedData) => {
        // Not specified in API docs provided, keeping placeholder or generic put
        try {
            set({ isUpdatingProfile: true });
            // const res = await axiosInstance.put("/auth/profile", updatedData);
            // set({ user: res.data });
        } catch (error) {
            console.log("error in edit profile:", error);
        } finally {
            set({ isUpdatingProfile: false });
        }
    },

    logout: async () => {
        try {
            set({ isLoggingOut: true });
            await axiosInstance.delete("/auth/logout");
            localStorage.removeItem("token");
            set({ user: null });
        } catch (error) {
            console.log("Error in logout", error);
        } finally {
            set({ isLoggingOut: false });
        }
    },

    resetPassword: async (email) => { // Changed param name for clarity if it's email
        try {
            set({ isUpdatingProfile: true }); // reusing loading state
            // await axiosInstance.post("/auth/reset-password", { email });
        } catch (error) {
            console.log("Error in reset password", error);
        } finally {
            set({ isUpdatingProfile: false });
        }
    },
}));

export default useAuthStore;

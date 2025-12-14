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
        } catch (error) {
        } finally {
            set({ isCheckingAuth: false });
        }
    },

    register: async (payload) => {
        try {
            set({ isRegistering: true });
        } catch (error) {
        } finally {
            set({ isRegistering: false });
        }
    },

    login: async (payload) => {
        try {
            set({ isLoggingIn: true });
        } catch (error) {
        } finally {
            set({ isLoggingIn: false });
        }
    },

    editProfile: async (updatedData) => {
        try {
            set({ isUpdatingProfile: true });
        } catch (error) {
        } finally {
            set({ isUpdatingProfile: false });
        }
    },

    logout: async () => {
        try {
            set({ isLoggingOut: true });
        } catch (error) {
        } finally {
            set({ isLoggingOut: false });
        }
    },

    resetPassword: async (password) => {
        try {
            set({ isUpdatingProfile: true });
        } catch (error) {
        } finally {
            set({ isUpdatingProfile: false });
        }
    },
}));

export default useAuthStore;

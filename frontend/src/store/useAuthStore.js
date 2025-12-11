import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useAuthStore = create((set, get) => ({
    user: null,
    isCheckingAuth: true,
    isRegistering: false,
    isLoggingIn: false,
    isUpdatingProfile: false,
    isLoggingOut: false,

    checkAuth: async () => {},

    register: async (payload) => {},

    login: async (payload) => {},

    editProfile: async (updatedData) => {},

    logout: async () => {},

    resetPassword: async (password) => {},
}));

export default useAuthStore;

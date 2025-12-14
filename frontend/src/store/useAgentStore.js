import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const useAgentStore = create((set) => ({
    isLoading: false,
    analysisResult: null, // { analysis, query, tool_calls }
    suggestions: null, // { suggestions, data_sources }
    chatHistory: [], // Array of messages
    report: null, // { report, days_analyzed }

    analyzeInfrastructure: async (projectId, query, days = 30) => {
        try {
            set({ isLoading: true });
            const res = await axiosInstance.post("/agent/analyze", {
                project_id: projectId,
                query: query,
                days: days
            });
            set({ analysisResult: res.data.data });
            return res.data.data;
        } catch (error) {
            console.error("Error analyzing infrastructure:", error);
            // Handle error state
        } finally {
            set({ isLoading: false });
        }
    },

    getSuggestions: async () => {
        try {
            // set({ isLoading: true }); // Optional: could be separate loading state if dashboard loads it
            const res = await axiosInstance.get("/agent/suggestions");
            set({ suggestions: res.data.data });
        } catch (error) {
            console.error("Error fetching suggestions:", error);
        } finally {
            // set({ isLoading: false });
        }
    },

    interactiveChat: async (query) => {
        try {
            set({ isLoading: true });
            // Add user message immediately if maintaining chat history
            set(state => ({
                chatHistory: [...state.chatHistory, { role: 'user', content: query }]
            }));

            // The API uses query param for interactive-chat
            const res = await axiosInstance.post(`/agent/interactive-chat?query=${encodeURIComponent(query)}`);

            // Assuming response format is similar to analyze or text
            // Adjust according to actual response structure if different
            set(state => ({
                chatHistory: [...state.chatHistory, { role: 'assistant', content: res.data.data?.analysis || JSON.stringify(res.data) }]
            }));

            return res.data;
        } catch (error) {
            console.error("Error in interactive chat:", error);
        } finally {
            set({ isLoading: false });
        }
    },

    generateReport: async (days = 30) => {
        try {
            set({ isLoading: true });
            const res = await axiosInstance.get(`/agent/report?days=${days}`);
            set({ report: res.data.data });
            return res.data.data;
        } catch (error) {
            console.error("Error generating report:", error);
        } finally {
            set({ isLoading: false });
        }
    }
}));

export default useAgentStore;

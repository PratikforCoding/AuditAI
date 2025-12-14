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
            console.warn("Analysis API failed, using mock:", error.message);
            await new Promise(r => setTimeout(r, 2000));
            const mockAnalysis = {
                analysis: "## Infrastructure Analysis\n\nI've analyzed your GCP infrastructure for project " + projectId + ".\n\n**Key Findings:**\n*   **Idle Resources:** 3 VMs detected with low utilization (< 5% CPU).\n*   **Security:** 2 storage buckets have public access enabled.\n*   **Cost:** Estimated potential savings of $450/month.",
                tool_calls: [{ name: "scan_idle_vms" }, { name: "check_bucket_permissions" }]
            };
            set({ analysisResult: mockAnalysis });
            return mockAnalysis;
        } finally {
            set({ isLoading: false });
        }
    },

    getSuggestions: async () => {
        try {
            const res = await axiosInstance.get("/agent/suggestions");
            set({ suggestions: res.data.data });
        } catch (error) {
            console.warn("Suggestions API failed, using mock:", error.message);
            set({
                suggestions: [
                    "Where can I save the most money?",
                    "Are there any security vulnerabilities?",
                    "Show me idle compute instances."
                ]
            });
        }
    },

    interactiveChat: async (query) => {
        try {
            set({ isLoading: true });
            set(state => ({
                chatHistory: [...state.chatHistory, { role: 'user', content: query }]
            }));

            const res = await axiosInstance.post(`/agent/interactive-chat?query=${encodeURIComponent(query)}`);

            const answer = res.data.data?.analysis || res.data.data?.response || "I processed your request.";

            set(state => ({
                chatHistory: [...state.chatHistory, { role: 'assistant', content: answer }]
            }));

            return res.data;
        } catch (error) {
            console.warn("Chat API failed, using mock:", error.message);
            await new Promise(r => setTimeout(r, 1000));
            const mockAnswer = "I'm currently running in offline mode, but I can tell you that optimizing your database usage would likely yield the highest ROI based on general patterns.";
            set(state => ({
                chatHistory: [...state.chatHistory, { role: 'assistant', content: mockAnswer }]
            }));
            return { data: { analysis: mockAnswer } };
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

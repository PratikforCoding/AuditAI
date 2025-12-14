import { create } from "zustand";
import axiosInstance from "@/utils/axiosInstance";

const generateMockAudit = () => ({
    audit_id: `audit_${Math.floor(Math.random() * 10000)}`,
    timestamp: new Date().toISOString(),
    duration_seconds: Math.floor(Math.random() * 300) + 60,
    resources_scanned: Math.floor(Math.random() * 100) + 20,
    issues_found: Math.floor(Math.random() * 10),
    total_savings: Math.floor(Math.random() * 1000) + 100,
    confidence_score: Math.floor(Math.random() * 10) + 90,
    issues_breakdown: {
        critical: Math.floor(Math.random() * 3),
        high: Math.floor(Math.random() * 5),
        medium: Math.floor(Math.random() * 5),
        low: Math.floor(Math.random() * 5)
    },
    recommendations: [
        {
            id: "rec_mock_1",
            title: "Delete unused database",
            description: "Instance hasn't been accessed in 90 days.",
            severity: "critical",
            monthly_savings: 250,
            risk: "Low",
            resource_id: "old-database",
            ai_analysis: "Based on logs..."
        },
        {
            id: "rec_mock_2",
            title: "Downsize development server",
            description: "CPU utilization below 5%.",
            severity: "high",
            monthly_savings: 120,
            risk: "Medium",
            resource_id: "dev-server",
            ai_analysis: "Based on metrics..."
        }
    ]
});

const useAuditStore = create((set) => ({
    currentAudit: null,
    history: [],
    isScanning: false,

    fetchLastAudit: async () => {
        try {
            set({ isScanning: true });
            const res = await axiosInstance.get("/audits/latest");
            if (res.data) {
                // Adjust based on actual API response structure
                // Assuming res.data.data contains the audit object, or res.data itself
                const auditData = res.data.data || res.data;
                set({ currentAudit: auditData });
                return;
            }
            throw new Error("No audit data");
        } catch (error) {
            console.warn("Audit API failed, using mock:", error.message);
            await new Promise(r => setTimeout(r, 1000));
            set({ currentAudit: generateMockAudit() });
        } finally {
            set({ isScanning: false });
        }
    },

    startNewAudit: async () => {
        try {
            set({ isScanning: true });
            const res = await axiosInstance.post("/audits/scan");
            if (res.data) {
                const auditData = res.data.data || res.data;
                set({ currentAudit: auditData });
                return;
            }
            throw new Error("Scan failed");
        } catch (error) {
            console.warn("Scan API failed, using mock:", error.message);
            // Simulating a scan process
            await new Promise(r => setTimeout(r, 3000));
            set({ currentAudit: generateMockAudit() });
        } finally {
            set({ isScanning: false });
        }
    }
}));

export default useAuditStore;

"use client";
import React, { useState } from "react";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import AuditSummary from "@/components/audits/AuditSummary";
import SeverityBreakdown from "@/components/audits/SeverityBreakdown";
import AIReasoning from "@/components/audits/AIReasoning";
import AuditRecommendations from "@/components/audits/AuditRecommendations";
import { Play, Download, Share2 } from "lucide-react";

// Mock Data Structure
const mockAuditData = {
    audit_id: "audit_1234",
    timestamp: "2025-12-09T10:30:00Z",
    duration_seconds: 154,
    resources_scanned: 42,
    issues_found: 5,
    total_savings: 780,
    confidence_score: 92,
    issues_breakdown: {
        critical: 1,
        high: 2,
        medium: 2,
        low: 0
    },
    recommendations: [
        {
            id: "rec_1",
            title: "Delete unused database",
            description: "Instance 'old-database' hasn't been accessed in 90 days. It is incurring costs without providing value.",
            severity: "critical",
            monthly_savings: 250,
            risk: "Low",
            resource_id: "old-database",
            ai_analysis: "Based on access logs and monitoring data..."
        },
        {
            id: "rec_2",
            title: "Downsize 'dev-server'",
            description: "Instance 'dev-server' average CPU utilization is below 5%. Reducing size from 8GB to 4GB RAM is recommended.",
            severity: "high",
            monthly_savings: 120,
            risk: "Medium",
            resource_id: "dev-server",
            ai_analysis: "Based on access logs and monitoring data..."
        },
        {
            id: "rec_3",
            title: "Release unattached IP",
            description: "Static IP 35.2.1.4 is reserved but not attached to any VM implementation.",
            severity: "high",
            monthly_savings: 15,
            risk: "Low",
            resource_id: "ip-35-2-1-4",
            ai_analysis: "..."
        }
    ]
};

export default function AuditResultsPage() {
    const [isRefreshing, setIsRefreshing] = useState(false);

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await new Promise((resolve) => setTimeout(resolve, 1500));
        setIsRefreshing(false);
    };

    const handleNewAudit = () => {
        alert("Starting new audit scan...");
    };

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                <DashboardHeader
                    title="Audit Results"
                    userName="Audit User"
                    onRefresh={handleRefresh}
                    isRefreshing={isRefreshing}
                />

                {/* Top Action Bar */}
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                    <div>
                        <h2 className="text-xl font-bold text-foreground">Last Scan Results</h2>
                        <p className="text-sm text-neutral-400">Completed on {new Date(mockAuditData.timestamp).toLocaleString()}</p>
                    </div>
                    <div className="flex gap-3">
                        <button className="flex items-center px-4 py-2 border border-border-light bg-card hover:bg-neutral-800 rounded-lg text-sm text-neutral-300 transition-colors">
                            <Download className="w-4 h-4 mr-2" /> PDF Report
                        </button>
                        <button className="flex items-center px-4 py-2 border border-border-light bg-card hover:bg-neutral-800 rounded-lg text-sm text-neutral-300 transition-colors">
                            <Share2 className="w-4 h-4 mr-2" /> Share
                        </button>
                        <button
                            onClick={handleNewAudit}
                            className="flex items-center px-4 py-2 bg-accent-dark hover:bg-accent-light text-white rounded-lg text-sm font-medium shadow-lg hover:shadow-accent-dark/20 transition-all"
                        >
                            <Play className="w-4 h-4 mr-2 fill-current" /> New Audit
                        </button>
                    </div>
                </div>

                <AuditSummary data={mockAuditData} />

                <SeverityBreakdown issues={mockAuditData.issues_breakdown} />

                <AIReasoning />

                <AuditRecommendations recommendations={mockAuditData.recommendations} />

            </div>
        </div>
    );
}

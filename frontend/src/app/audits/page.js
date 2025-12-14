"use client";
import React, { useState } from "react";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import AuditSummary from "@/components/audits/AuditSummary";
import SeverityBreakdown from "@/components/audits/SeverityBreakdown";
import AIReasoning from "@/components/audits/AIReasoning";
import AuditRecommendations from "@/components/audits/AuditRecommendations";
import { Play, Download, Share2 } from "lucide-react";

import useAuditStore from "@/store/useAuditStore";
import { useEffect } from "react";

export default function AuditResultsPage() {
    const {
        currentAudit,
        isScanning: isRefreshing,
        fetchLastAudit,
        startNewAudit
    } = useAuditStore();

    useEffect(() => {
        fetchLastAudit();

        // Auto-refresh every 15 seconds
        const interval = setInterval(() => {
            fetchLastAudit();
        }, 15000);

        return () => clearInterval(interval);
    }, []);

    const handleRefresh = async () => {
        await fetchLastAudit();
    };

    const handleNewAudit = async () => {
        await startNewAudit();
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
                        <p className="text-sm text-neutral-400">
                            {currentAudit ? `Completed on ${new Date(currentAudit.timestamp).toLocaleString()}` : "No audit history found"}
                        </p>
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
                            disabled={isRefreshing}
                            className="flex items-center px-4 py-2 bg-accent-dark hover:bg-accent-light text-white rounded-lg text-sm font-medium shadow-lg hover:shadow-accent-dark/20 transition-all disabled:opacity-50"
                        >
                            <Play className="w-4 h-4 mr-2 fill-current" /> {isRefreshing ? "Scanning..." : "New Audit"}
                        </button>
                    </div>
                </div>

                {currentAudit ? (
                    <>
                        <AuditSummary data={currentAudit} />
                        <SeverityBreakdown issues={currentAudit.issues_breakdown} />
                        <AIReasoning />
                        <AuditRecommendations recommendations={currentAudit.recommendations} />
                    </>
                ) : (
                    <div className="text-center py-20 text-neutral-500">
                        No audit data available. Start a new audit to see results.
                    </div>
                )}

            </div>
        </div>
    );
}

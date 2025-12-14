"use client";
import React, { useState, useEffect, useMemo, useCallback } from "react";
import {
    Users,
    Server,
    Zap,
    Clock,
    DollarSign,
    TrendingDown,
    RefreshCw,
    User2,
    LogOut,
    ChevronDown,
    ChevronUp,
    AlertTriangle,
    Play,
} from "lucide-react";
import MetricCard from "@/components/dashboard-components/MetricCard";
import RecentAuditsTable from "@/components/dashboard-components/RecentAuditsTable";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import DashboardLoader from "@/components/dashboard-components/DashboardLoader";
import useDashboardStore from "@/store/useDashboardStore";

// Removed initialMockData

//Helper function to calculate time difference
const timeSince = (dateString) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + " years ago";
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + " months ago";
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + " days ago";
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + " hours ago";
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + " minutes ago";
    return Math.floor(seconds) + " seconds ago";
};

const DashboardPage = () => {
    const { summaryData, isDashboardLoading: loading, fetchDashboardData } = useDashboardStore();
    const [isRefreshing, setIsRefreshing] = useState(false);

    // Mock fetching data from /api/status or similar
    const fetchData = useCallback(async () => {
        setIsRefreshing(true);
        console.log("Fetching dashboard data...");
        await fetchDashboardData();
        setIsRefreshing(false);
    }, [fetchDashboardData]);

    useEffect(() => {
        fetchData();

        // Auto-refresh every 20 seconds
        const interval = setInterval(() => {
            fetchData();
        }, 20000);

        return () => clearInterval(interval);
    }, [fetchData]);

    const data = summaryData || { // Fallback to safe defaults or skeletons if null
        total_resources: 0,
        running_instances: 0,
        idle_resources: 0,
        monthly_cost: 0,
        potential_savings: 0,
        recent_audits: []
    };

    const handleRunAudit = () => {
        // This would trigger a POST /api/audit
        console.log("Triggering new Audit via POST /api/audit");
        // Mock response for user feedback
        alert(
            "Audit has been successfully triggered! Results will appear soon.",
        );
    };

    const auditTimeAgo = data ? timeSince(data.last_audit) : "";

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                {/* Header and User Controls */}
                <DashboardHeader
                    title="Dashboard"
                    userName={data?.user?.name || "Loading..."}
                    onRefresh={fetchData}
                    isRefreshing={isRefreshing}
                />

                {loading ? (
                    <DashboardLoader />
                ) : (
                    <>
                        {/* Quick Stats Grid */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
                            <MetricCard
                                title="Total Resources"
                                value={data.total_resources}
                                icon={Server}
                                colorClass="text-accent-dark"
                            />
                            <MetricCard
                                title="Running Instances"
                                value={data.running_instances}
                                icon={Zap}
                                colorClass="text-status-running"
                            />
                            <MetricCard
                                title="Idle Resources"
                                value={data.idle_resources}
                                icon={Clock}
                                colorClass="text-yellow-400"
                            />
                            <MetricCard
                                title="Monthly Cost"
                                value={`$${data.monthly_cost.toLocaleString()}`}
                                icon={DollarSign}
                                colorClass="text-green-600"
                            />
                            <MetricCard
                                title="Potential Savings"
                                value={`$${data.potential_savings.toLocaleString()}`}
                                icon={TrendingDown}
                                colorClass="text-pink-400"
                            />
                            <MetricCard
                                title="Last Audit"
                                value={auditTimeAgo}
                                icon={Clock}
                                colorClass="text-neutral-400"
                            />
                        </div>

                        {/* Run Audit Button */}
                        <div className="mt-8 flex justify-end">
                            <button
                                onClick={handleRunAudit}
                                className="flex items-center px-6 py-3 font-semibold text-foreground bg-accent-dark/70 rounded-md shadow-none hover:bg-accent-dark duration-200 focus:outline-none"
                            >
                                <Play className="w-5 h-5 mr-2 fill-white" />
                                Run Audit Now
                            </button>
                        </div>

                        {/* Recent Audits Table */}
                        <RecentAuditsTable audits={data.recent_audits} />
                    </>
                )}
            </div>
        </div>
    );
};

export default DashboardPage;

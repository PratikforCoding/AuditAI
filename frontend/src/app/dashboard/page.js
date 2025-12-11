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

const initialMockData = {
    user: { name: "Audit User" },
    total_resources: 42,
    running_instances: 8,
    idle_resources: 34,
    monthly_cost: 2450,
    potential_savings: 780,
    last_audit: "2025-12-09T10:30:00Z",
    recent_audits: [
        {
            id: "audit_1",
            date: "2025-12-09",
            resources_scanned: 42,
            issues_found: 5,
            savings: 240,
        },
        {
            id: "audit_2",
            date: "2025-12-08",
            resources_scanned: 40,
            issues_found: 0,
            savings: 180,
        },
        {
            id: "audit_3",
            date: "2025-12-07",
            resources_scanned: 38,
            issues_found: 7,
            savings: 360,
        },
        {
            id: "audit_4",
            date: "2025-12-06",
            resources_scanned: 35,
            issues_found: 2,
            savings: 100,
        },
    ],
};

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
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isRefreshing, setIsRefreshing] = useState(false);

    // Mock fetching data from /api/status or similar
    const fetchData = useCallback(async () => {
        setLoading(true);
        setIsRefreshing(true);
        console.log("Fetching dashboard data from /api/status...");

        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 1500));

        // In a real app, replace this with a fetch call:
        // const response = await fetch('/api/status');
        // const result = await response.json();
        // setData(result.data);

        setData(initialMockData);
        setLoading(false);
        setIsRefreshing(false);
        console.log("Dashboard data loaded.");
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

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

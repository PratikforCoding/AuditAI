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

    if (loading) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center p-4">
                <div className="text-center">
                    <svg
                        className="animate-spin h-10 w-10 text-accent-dark mx-auto mb-4"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                    >
                        <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                        ></circle>
                        <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                    </svg>
                    <p className="text-foreground text-xl">
                        Loading AuditAI Dashboard...
                    </p>
                </div>
            </div>
        );
    }

    const auditTimeAgo = timeSince(data.last_audit);

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                {/* Header and User Controls */}
                <header className="flex justify-between items-center pb-6 border-b border-border-light mb-6">
                    <h1 className="text-3xl font-extrabold text-foreground">
                        Audit<span className="text-accent-dark mr-3">AI</span>
                        Dashboard
                    </h1>
                    <div className="flex items-center space-x-4">
                        <p className="hidden md:block text-lg font-medium text-foreground">
                            Hello, {data.user.name}!
                        </p>

                        {/* Refresh Button */}
                        <button
                            onClick={fetchData}
                            disabled={isRefreshing}
                            className={`p-2 rounded-full border border-neutral-800 bg-[#080808] text-pink-400 hover:bg-neutral-800 transition-duration-200 ${
                                isRefreshing
                                    ? "opacity-70 cursor-not-allowed"
                                    : "hover:border-accent-light"
                            }`}
                            title="Refresh Data"
                        >
                            <RefreshCw
                                className={`w-5 h-5 ${
                                    isRefreshing ? "animate-spin" : ""
                                }`}
                            />
                        </button>

                        {/* User Profile/Dropdown Placeholder */}
                        <div className="relative group">
                            <button className="flex items-center p-2 rounded-full border border-border-light bg-accent-dark text-foreground hover:bg-accent-light duration-200">
                                <User2 className="w-5 h-5" />
                            </button>
                            {/* Mock Dropdown Menu */}
                            <div className="absolute right-0 mt-2 w-48 bg-[#1A1A1A] border border-neutral-800 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
                                <a
                                    href="#"
                                    onClick={(e) => {
                                        e.preventDefault();
                                        console.log("View Profile clicked");
                                    }}
                                    className="flex items-center px-4 py-2 text-neutral-300 hover:bg-neutral-800 rounded-t-lg"
                                >
                                    <User2 className="w-4 h-4 mr-2" /> Profile
                                </a>
                                <a
                                    href="#"
                                    onClick={(e) => {
                                        e.preventDefault();
                                        console.log("Logout clicked");
                                    }}
                                    className="flex items-center px-4 py-2 text-red-400 hover:bg-red-900/30 rounded-b-lg border-t border-neutral-800"
                                >
                                    <LogOut className="w-4 h-4 mr-2" /> Logout
                                </a>
                            </div>
                        </div>
                    </div>
                </header>

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
            </div>
        </div>
    );
};

export default DashboardPage;

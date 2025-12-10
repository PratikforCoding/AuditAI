"use client";
import React, { useState } from "react";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import CostTrendChart from "@/components/analytics/CostTrendChart";
import CostDistributionChart from "@/components/analytics/CostDistributionChart";
import TopResourcesTable from "@/components/analytics/TopResourcesTable";
import SavingsCard from "@/components/analytics/SavingsCard";
import { Download, Calendar } from "lucide-react";

export default function AnalyticsPage() {
    const [isRefreshing, setIsRefreshing] = useState(false);

    const handleRefresh = async () => {
        setIsRefreshing(true);
        // Simulate refresh
        await new Promise((resolve) => setTimeout(resolve, 1500));
        setIsRefreshing(false);
    };

    const handleExport = () => {
        alert("Exporting report... (This is a mock action)");
        console.log("Export triggered");
    };

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                <DashboardHeader
                    title="Analytics"
                    userName="Audit User" // In real app, get from context/store
                    onRefresh={handleRefresh}
                    isRefreshing={isRefreshing}
                />

                {/* Toolbar */}
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-xl font-semibold text-foreground">
                        Cost Overview
                    </h2>
                    <div className="flex gap-3">
                        <button className="flex items-center px-4 py-2 bg-card border border-border-light rounded-lg text-sm font-medium text-foreground hover:bg-neutral-800 transition-colors">
                            <Calendar className="w-4 h-4 mr-2 text-neutral-400" />
                            This Month
                        </button>
                        <button
                            onClick={handleExport}
                            className="flex items-center px-4 py-2 bg-card border border-border-light rounded-lg text-sm font-medium text-foreground hover:bg-neutral-800 transition-colors"
                        >
                            <Download className="w-4 h-4 mr-2 text-neutral-400" />
                            Export
                        </button>
                    </div>
                </div>

                {/* Main Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                    {/* Cost Trend - Takes 2 columns on large screens */}
                    <div className="lg:col-span-2">
                        <CostTrendChart />
                    </div>
                    {/* Cost Distribution - Takes 1 column */}
                    <div className="lg:col-span-1">
                        <CostDistributionChart />
                    </div>
                </div>

                {/* Secondary Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Top Resources - Takes 2 columns */}
                    <div className="lg:col-span-2">
                        <TopResourcesTable />
                    </div>
                    {/* Savings Card - Takes 1 column */}
                    <div className="lg:col-span-1">
                        <SavingsCard />
                    </div>
                </div>
            </div>
        </div>
    );
}

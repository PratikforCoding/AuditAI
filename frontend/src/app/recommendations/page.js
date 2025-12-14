"use client";
import React, { useState, useMemo } from "react";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import SummaryStats from "@/components/recommendations/SummaryStats";
import ActionItemCard from "@/components/recommendations/ActionItemCard";
import AppliedLog from "@/components/recommendations/AppliedLog";
import FilterBar from "@/components/recommendations/FilterBar";

// Mock Data
const initialRecommendations = [
    {
        id: "rec_1",
        title: "Delete unused-vm-3",
        type: "Compute",
        savings: 150,
        risk: "Low",
        difficulty: "Easy",
        daysIdle: 45,
        description: "This VM has been idle for over 45 days. Consistently low CPU and network activity suggests it is no longer in use.",
    },
    {
        id: "rec_2",
        title: "Resize prod-db 16→8GB RAM",
        type: "Database",
        savings: 320,
        risk: "Medium",
        difficulty: "Medium",
        usage: "25%",
        description: "Database memory utilization peaks at 25%. Downsizing to 8GB RAM instance type will maintain performance headroom while reducing costs.",
    },
    {
        id: "rec_3",
        title: "Archive old-storage bucket",
        type: "Storage",
        savings: 80,
        risk: "Low",
        difficulty: "Easy",
        size: "500GB",
        description: "Access logs show no read/write operations in the last 90 days. Moving to Coldline storage is recommended.",
    },
    {
        id: "rec_4",
        title: "Release unattached IP 34.12.1.20",
        type: "Network",
        savings: 15,
        risk: "Low",
        difficulty: "Easy",
        daysIdle: 20,
        description: "Static IP address is reserved but not attached to any resource.",
    },
    {
        id: "rec_5",
        title: "Spot Instance Migration for Batch Jobs",
        type: "Compute",
        savings: 450,
        risk: "High",
        difficulty: "Hard",
        description: "Migrate non-critical batch processing workloads to Spot Instances for up to 60-90% savings. Requires fault-tolerant architecture.",
    }
];

const initialApplied = [
    {
        id: "app_1",
        title: "Deleted old-database",
        type: "Database",
        risk: "Low",
        savings: 250,
        appliedDate: "Dec 8, 2025",
    },
    {
        id: "app_2",
        title: "Downsized dev-1 VM",
        type: "Compute",
        risk: "Low",
        savings: 80,
        appliedDate: "Dec 7, 2025",
    }
];

export default function RecommendationsPage() {
    const [recommendations, setRecommendations] = useState(initialRecommendations);
    const [appliedItems, setAppliedItems] = useState(initialApplied);
    const [isRefreshing, setIsRefreshing] = useState(false);

    // Filters
    const [filterStatus, setFilterStatus] = useState("all"); // 'all', 'pending' (Note: 'applied' are in separate list)
    const [filterSeverity, setFilterSeverity] = useState("all");
    const [sortBy, setSortBy] = useState("savings-desc");

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        // In real app, re-fetch data here
        setIsRefreshing(false);
    };

    const handleApply = (id) => {
        const itemToApply = recommendations.find(r => r.id === id);
        if (itemToApply) {
            // Remove from recommendations
            setRecommendations(prev => prev.filter(r => r.id !== id));

            // Add to applied list with current date
            const newItem = {
                ...itemToApply,
                appliedDate: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
            };
            setAppliedItems(prev => [newItem, ...prev]);
        }
    };

    // Filter and Sort Logic
    const filteredRecommendations = useMemo(() => {
        let result = [...recommendations];

        // Filter by Risk
        if (filterSeverity !== "all") {
            result = result.filter(item => item.risk === filterSeverity);
        }

        // Sort
        result.sort((a, b) => {
            switch (sortBy) {
                case "savings-desc": return b.savings - a.savings;
                case "savings-asc": return a.savings - b.savings;
                case "risk-desc":
                    const riskOrder = { "High": 3, "Medium": 2, "Low": 1 };
                    return riskOrder[b.risk] - riskOrder[a.risk];
                case "risk-asc":
                    const riskOrderAsc = { "High": 3, "Medium": 2, "Low": 1 };
                    return riskOrderAsc[a.risk] - riskOrderAsc[b.risk];
                default: return 0;
            }
        });

        return result;
    }, [recommendations, filterSeverity, sortBy]);

    // Calculate Stats
    const stats = useMemo(() => {
        const totalSavings = initialRecommendations.reduce((acc, curr) => acc + curr.savings, 0); // Total potential from start (or current?)
        // Let's make total savings reflect CURRENT potential
        const currentPotential = recommendations.reduce((acc, curr) => acc + curr.savings, 0);

        return {
            totalSavings: currentPotential,
            pendingCount: recommendations.length,
            completedCount: appliedItems.length
        };
    }, [recommendations, appliedItems]);

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                <DashboardHeader
                    title="Recommendations"
                    userName="Audit User"
                    onRefresh={handleRefresh}
                    isRefreshing={isRefreshing}
                />

                <SummaryStats stats={stats} />

                <div className="mb-8">
                    <h2 className="text-xl font-semibold text-foreground mb-4">Action Items</h2>

                    <FilterBar
                        filterStatus={filterStatus}
                        setFilterStatus={setFilterStatus}
                        filterSeverity={filterSeverity}
                        setFilterSeverity={setFilterSeverity}
                        sortBy={sortBy}
                        setSortBy={setSortBy}
                    />

                    <div className="space-y-4">
                        {filteredRecommendations.length > 0 ? (
                            filteredRecommendations.map(item => (
                                <ActionItemCard
                                    key={item.id}
                                    item={item}
                                    onApply={handleApply}
                                />
                            ))
                        ) : (
                            <div className="p-8 text-center bg-card border border-border-light rounded-xl text-neutral-500">
                                No recommendations found matching your filters.
                            </div>
                        )}
                    </div>
                </div>

                <div>
                    <AppliedLog appliedItems={appliedItems} />
                </div>
            </div>
        </div>
    );
}

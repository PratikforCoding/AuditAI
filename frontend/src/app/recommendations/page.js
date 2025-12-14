"use client";
import React, { useState, useMemo } from "react";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import SummaryStats from "@/components/recommendations/SummaryStats";
import ActionItemCard from "@/components/recommendations/ActionItemCard";
import AppliedLog from "@/components/recommendations/AppliedLog";
import FilterBar from "@/components/recommendations/FilterBar";

import useRecommendationStore from "@/store/useRecommendationStore";
import { useEffect } from "react";

export default function RecommendationsPage() {
    const {
        recommendations,
        appliedItems,
        isLoading: isRefreshing,
        fetchRecommendations,
        applyRecommendation
    } = useRecommendationStore();

    useEffect(() => {
        fetchRecommendations();

        // Auto-refresh every 12 seconds
        const interval = setInterval(() => {
            fetchRecommendations();
        }, 12000);

        return () => clearInterval(interval);
    }, []);

    const handleRefresh = async () => {
        await fetchRecommendations();
    };

    const handleApply = (id) => {
        applyRecommendation(id);
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

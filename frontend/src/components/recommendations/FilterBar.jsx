"use client";
import React from "react";
import { Filter, SlidersHorizontal } from "lucide-react";

export default function FilterBar({
    filterStatus,
    setFilterStatus,
    filterSeverity,
    setFilterSeverity,
    sortBy,
    setSortBy
}) {
    return (
        <div className="flex flex-col sm:flex-row gap-4 justify-between items-center mb-6">
            <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0 hide-scrollbar">
                <div className="flex items-center gap-2 px-3 py-2 bg-card border border-border-light rounded-lg">
                    <Filter className="w-4 h-4 text-neutral-500" />
                    <span className="text-sm font-medium text-neutral-400 mr-2">Status:</span>
                    <select
                        value={filterStatus}
                        onChange={(e) => setFilterStatus(e.target.value)}
                        className="bg-transparent text-sm text-foreground focus:outline-none cursor-pointer"
                    >
                        <option value="all">All</option>
                        <option value="pending">Pending</option>
                    </select>
                </div>

                <div className="flex items-center gap-2 px-3 py-2 bg-card border border-border-light rounded-lg">
                    <Filter className="w-4 h-4 text-neutral-500" />
                    <span className="text-sm font-medium text-neutral-400 mr-2">Risk:</span>
                    <select
                        value={filterSeverity}
                        onChange={(e) => setFilterSeverity(e.target.value)}
                        className="bg-transparent text-sm text-foreground focus:outline-none cursor-pointer"
                    >
                        <option value="all">All Risks</option>
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                    </select>
                </div>
            </div>

            <div className="flex items-center gap-2 w-full sm:w-auto">
                <div className="flex items-center gap-2 px-3 py-2 bg-card border border-border-light rounded-lg w-full sm:w-auto">
                    <SlidersHorizontal className="w-4 h-4 text-neutral-500" />
                    <span className="text-sm font-medium text-neutral-400 mr-2 whitespace-nowrap">Sort by:</span>
                    <select
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value)}
                        className="bg-transparent text-sm text-foreground focus:outline-none cursor-pointer w-full"
                    >
                        <option value="savings-desc">Savings (High to Low)</option>
                        <option value="savings-asc">Savings (Low to High)</option>
                        <option value="risk-desc">Risk (High to Low)</option>
                        <option value="risk-asc">Risk (Low to High)</option>
                    </select>
                </div>
            </div>
        </div>
    );
}

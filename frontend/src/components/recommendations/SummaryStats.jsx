"use client";
import React from "react";
import { DollarSign, Clock, CheckCircle2 } from "lucide-react";

const StatCard = ({ title, value, subtext, icon: Icon, colorClass, bgClass }) => (
    <div className={`p-6 rounded-xl border ${bgClass} border-border-light flex items-center space-x-4`}>
        <div className={`p-3 rounded-lg ${colorClass} bg-opacity-20`}>
            <Icon className={`w-6 h-6 ${colorClass} text-opacity-100`} />
        </div>
        <div>
            <p className="text-sm font-medium text-neutral-400">{title}</p>
            <h4 className="text-2xl font-bold text-foreground mt-1">{value}</h4>
            {subtext && <p className="text-xs text-neutral-500 mt-1">{subtext}</p>}
        </div>
    </div>
);

export default function SummaryStats({ stats }) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <StatCard
                title="Total Potential Savings"
                value={`$${stats.totalSavings}/mo`}
                subtext="Across all pending actions"
                icon={DollarSign}
                colorClass="text-green-500"
                bgClass="bg-[#0e0e0e]"
            />
            <StatCard
                title="Pending Actions"
                value={`${stats.pendingCount} actions`}
                subtext="Waiting for approval"
                icon={Clock}
                colorClass="text-yellow-500"
                bgClass="bg-[#0e0e0e]"
            />
            <StatCard
                title="Completed Actions"
                value={`${stats.completedCount} actions`}
                subtext="successfully applied"
                icon={CheckCircle2}
                colorClass="text-accent-light"
                bgClass="bg-[#0e0e0e]"
            />
        </div>
    );
}

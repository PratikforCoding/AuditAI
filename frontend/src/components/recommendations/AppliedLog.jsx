"use client";
import React from "react";
import { CheckCircle2, History } from "lucide-react";

export default function AppliedLog({ appliedItems }) {
    if (appliedItems.length === 0) {
        return (
            <div className="bg-card border border-border-light rounded-xl p-8 text-center">
                <div className="inline-flex p-3 rounded-full bg-neutral-900 mb-4">
                    <History className="w-6 h-6 text-neutral-600" />
                </div>
                <h3 className="text-lg font-medium text-foreground">No Applied Recommendations Yet</h3>
                <p className="text-neutral-500 mt-2">Actions you take will appear here for tracking.</p>
            </div>
        );
    }

    return (
        <div className="bg-card border border-border-light rounded-xl overflow-hidden shadow-sm">
            <div className="p-6 border-b border-border-light bg-[#141414]">
                <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5 text-accent-light" />
                    Applied Recommendations History
                </h3>
            </div>
            <div className="divide-y divide-neutral-800">
                {appliedItems.map((item) => (
                    <div key={item.id} className="p-4 hover:bg-neutral-900/30 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <h4 className="font-medium text-neutral-300 line-through decoration-neutral-600 decoration-2">{item.title}</h4>
                                <span className="text-xs text-neutral-500 bg-neutral-900 border border-neutral-800 px-2 py-0.5 rounded">
                                    Applied: {item.appliedDate}
                                </span>
                            </div>
                            <p className="text-sm text-neutral-500">
                                {item.type} • {item.risk} Risk
                            </p>
                        </div>
                        <div className="flex items-center gap-6">
                            <div className="text-right">
                                <p className="text-xs text-neutral-500">Projected Savings</p>
                                <p className="text-sm font-semibold text-neutral-400">${item.savings}/mo</p>
                            </div>
                            <div className="text-right">
                                <p className="text-xs text-neutral-500">Actual Savings</p>
                                <p className="text-lg font-bold text-green-500">${item.savings}/mo</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

"use client";
import React from "react";

export default function SeverityBreakdown({ issues }) {
    // Determine counts mock or real
    // Assuming passed props might be like { critical: 1, high: 2, ... }
    // But aligning with user request: "Issues by Severity"

    // Default to 0 if undefined
    const { critical = 0, high = 0, medium = 0, low = 0 } = issues || {};

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 flex items-center justify-between">
                <div>
                    <p className="text-red-400 text-xs font-bold uppercase tracking-wider">Critical</p>
                    <p className="text-2xl font-bold text-red-100">{critical}</p>
                </div>
                <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse"></div>
            </div>

            <div className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3 flex items-center justify-between">
                <div>
                    <p className="text-orange-400 text-xs font-bold uppercase tracking-wider">High</p>
                    <p className="text-2xl font-bold text-orange-100">{high}</p>
                </div>
                <div className="h-2 w-2 rounded-full bg-orange-500"></div>
            </div>

            <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 flex items-center justify-between">
                <div>
                    <p className="text-yellow-400 text-xs font-bold uppercase tracking-wider">Medium</p>
                    <p className="text-2xl font-bold text-yellow-100">{medium}</p>
                </div>
                <div className="h-2 w-2 rounded-full bg-yellow-500"></div>
            </div>

            <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3 flex items-center justify-between">
                <div>
                    <p className="text-blue-400 text-xs font-bold uppercase tracking-wider">Low</p>
                    <p className="text-2xl font-bold text-blue-100">{low}</p>
                </div>
                <div className="h-2 w-2 rounded-full bg-blue-500"></div>
            </div>
        </div>
    );
}

"use client";
import React from "react";
import { AlertTriangle, Activity } from "lucide-react";

export default function ThresholdsSettings() {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-2">
                <Activity className="w-5 h-5 text-accent-light" />
                Alert Thresholds
            </h3>
            <p className="text-sm text-neutral-400 mb-6">
                Configure when resources should be flagged as underutilized or critical.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="space-y-2">
                    <label className="block text-sm font-medium text-neutral-300">
                        High CPU Usage {'>'}
                    </label>
                    <div className="relative">
                        <input
                            type="number"
                            defaultValue={70}
                            className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all"
                        />
                        <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-neutral-500">%</span>
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="block text-sm font-medium text-neutral-300">
                        High Memory Usage {'>'}
                    </label>
                    <div className="relative">
                        <input
                            type="number"
                            defaultValue={80}
                            className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all"
                        />
                        <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-neutral-500">%</span>
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="block text-sm font-medium text-neutral-300">
                        High Disk Usage {'>'}
                    </label>
                    <div className="relative">
                        <input
                            type="number"
                            defaultValue={85}
                            className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all"
                        />
                        <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-neutral-500">%</span>
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="block text-sm font-medium text-neutral-300">
                        Identify Idle Resources after
                    </label>
                    <div className="relative">
                        <input
                            type="number"
                            defaultValue={30}
                            className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all"
                        />
                        <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-neutral-500">days</span>
                    </div>
                </div>
            </div>

            <div className="mt-6 p-4 bg-yellow-500/5 border border-yellow-500/20 rounded-lg flex gap-3 text-yellow-500/80 text-sm">
                <AlertTriangle className="w-5 h-5 flex-shrink-0" />
                <p>Lower thresholds may increase false positives, while higher thresholds might miss some optimization opportunities.</p>
            </div>
        </div>
    );
}

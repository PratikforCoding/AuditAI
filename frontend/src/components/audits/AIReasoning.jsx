"use client";
import React, { useState } from "react";
import { Sparkles, ChevronDown, ChevronUp } from "lucide-react";

export default function AIReasoning() {
    const [isExpanded, setIsExpanded] = useState(true);

    return (
        <div className="mb-8 rounded-xl bg-gradient-to-r from-[#1A1A1A] to-[#141414] border border-border-light overflow-hidden">
            <div
                className="p-4 flex items-center justify-between cursor-pointer hover:bg-white/5 transition-colors"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-purple-500/20 rounded-lg">
                        <Sparkles className="w-5 h-5 text-purple-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-foreground">AI Analysis & Reasoning</h3>
                </div>
                {isExpanded ? <ChevronUp className="w-5 h-5 text-neutral-400" /> : <ChevronDown className="w-5 h-5 text-neutral-400" />}
            </div>

            {isExpanded && (
                <div className="px-4 pb-6 pt-0 sm:px-14">
                    <div className="prose prose-invert max-w-none text-neutral-300">
                        <p className="mb-4">
                            Based on the scan of <strong>42 resources</strong> across your GCP project <code>audit-ai-prod</code>,
                            I&apos;ve detected significant optimization opportunities primarily in compute and storage layers.
                        </p>
                        <ul className="list-disc pl-5 space-y-2 mb-4">
                            <li>
                                <span className="text-red-400 font-medium">Critical Inefficiency:</span> The database instance <code>old-database</code>
                                has shown <strong>0 connections</strong> for the past 90 days. Decommissioning this will yield immediate savings.
                            </li>
                            <li>
                                <span className="text-orange-400 font-medium">Oversized Compute:</span> <code>dev-server</code> is utilizing only
                                <strong>12% of its RAM</strong> on average. Downsizing to an <code>n1-standard-1</code> is safe given the load patterns.
                            </li>
                        </ul>
                        <p className="text-sm text-neutral-500 mt-4 border-t border-white/5 pt-4">
                            Analysis completed in 2.5s with 92% confidence score.
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}

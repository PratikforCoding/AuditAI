"use client";
import React, { useState } from "react";
import { AlertTriangle, Check, ChevronDown, ChevronUp, DollarSign, Database, Server, Box } from "lucide-react";

export default function ActionItemCard({ item, onApply }) {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isApplying, setIsApplying] = useState(false);

    const handleApply = async () => {
        setIsApplying(true);
        // Simulate delay
        await new Promise(resolve => setTimeout(resolve, 800));
        onApply(item.id);
        setIsApplying(false);
    };

    const getDifficultyColor = (diff) => {
        switch (diff.toLowerCase()) {
            case 'easy': return 'text-green-400 bg-green-400/10 border-green-400/20';
            case 'medium': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
            case 'hard': return 'text-red-400 bg-red-400/10 border-red-400/20';
            default: return 'text-neutral-400 bg-neutral-800 border-neutral-700';
        }
    };

    const getRiskColor = (risk) => {
        switch (risk.toLowerCase()) {
            case 'low': return 'text-green-400';
            case 'medium': return 'text-yellow-400';
            case 'high': return 'text-red-400';
            default: return 'text-neutral-400';
        }
    };

    const Icon = item.type === 'Database' ? Database : item.type === 'Compute' ? Server : Box;

    return (
        <div className="bg-card border border-border-light rounded-xl overflow-hidden transition-all duration-200 hover:border-neutral-700">
            <div className="p-5 flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
                <div className="flex items-start gap-4">
                    <div className="mt-1 p-2 bg-neutral-900 rounded-lg">
                        <Icon className="w-5 h-5 text-accent-light" />
                    </div>
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <h4 className="text-lg font-semibold text-foreground">{item.title}</h4>
                            <span className={`px-2 py-0.5 text-xs font-medium rounded border ${getDifficultyColor(item.difficulty)}`}>
                                {item.difficulty}
                            </span>
                        </div>
                        <div className="flex flex-wrap gap-x-4 gap-y-1 text-sm text-neutral-400">
                            <span className="flex items-center gap-1">
                                Risk: <span className={getRiskColor(item.risk)}>{item.risk}</span>
                            </span>
                            {item.daysIdle && (
                                <span>• {item.daysIdle} Days Idle</span>
                            )}
                            {item.usage && (
                                <span>• {item.usage} Usage</span>
                            )}
                            {item.size && (
                                <span>• {item.size}</span>
                            )}
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-end">
                    <div className="text-right">
                        <p className="text-xs text-neutral-500 uppercase font-medium">Potential Savings</p>
                        <p className="text-xl font-bold text-green-400">${item.savings}</p>
                    </div>

                    <button
                        onClick={handleApply}
                        disabled={isApplying}
                        className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${isApplying
                                ? 'bg-neutral-800 text-neutral-500 cursor-not-allowed'
                                : 'bg-accent-dark hover:bg-accent-light text-white shadow-lg hover:shadow-accent-dark/20'
                            }`}
                    >
                        {isApplying ? (
                            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                        ) : (
                            <Check className="w-4 h-4" />
                        )}
                        <span className="hidden sm:inline">Apply</span>
                    </button>

                    <button
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="p-2 text-neutral-500 hover:text-white transition-colors"
                    >
                        {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                    </button>
                </div>
            </div>

            {/* Expanded Details */}
            {isExpanded && (
                <div className="px-5 pb-5 pt-0 border-t border-neutral-800/50 mt-2">
                    <div className="pt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h5 className="text-sm font-medium text-neutral-300 mb-2">Recommendation Detail</h5>
                            <p className="text-sm text-neutral-400 leading-relaxed">
                                {item.description || "No additional description available for this recommendation."}
                            </p>
                        </div>
                        <div>
                            <h5 className="text-sm font-medium text-neutral-300 mb-2">Impact Analysis</h5>
                            <ul className="text-sm text-neutral-400 space-y-1">
                                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-neutral-600"></div> No downtime expected</li>
                                <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-neutral-600"></div> Reversible via backup snapshot</li>
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

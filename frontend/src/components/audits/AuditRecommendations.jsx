"use client";
import React, { useState } from "react";
import { Check, Info, Trash2 } from "lucide-react";

const RecommendationItem = ({ item }) => {
    const [status, setStatus] = useState("pending"); // pending, applied, dismissed

    if (status === "dismissed") return null;

    const getSeverityColor = (sev) => {
        switch (sev.toLowerCase()) {
            case 'critical': return 'text-red-400 border-red-500/50 bg-red-500/10';
            case 'high': return 'text-orange-400 border-orange-500/50 bg-orange-500/10';
            case 'medium': return 'text-yellow-400 border-yellow-500/50 bg-yellow-500/10';
            default: return 'text-blue-400 border-blue-500/50 bg-blue-500/10';
        }
    };

    return (
        <div className={`p-4 rounded-lg bg-card border border-border-light hover:border-neutral-700 transition-all ${status === 'applied' ? 'opacity-50' : ''}`}>
            <div className="flex flex-col sm:flex-row gap-4 justify-between">

                {/* Left Content */}
                <div className="flex gap-4">
                    <div className="mt-1">
                        {status === 'applied' ? (
                            <div className="bg-green-500/20 p-2 rounded-full">
                                <Check className="w-5 h-5 text-green-500" />
                            </div>
                        ) : (
                            <span className={`inline-flex items-center justify-center px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wider border ${getSeverityColor(item.severity)}`}>
                                {item.severity}
                            </span>
                        )}
                    </div>
                    <div>
                        <h4 className={`text-lg font-semibold text-foreground ${status === 'applied' ? 'line-through text-neutral-500' : ''}`}>{item.title}</h4>
                        <p className="text-sm text-neutral-400 mt-1">{item.description}</p>

                        <div className="flex flex-wrap gap-4 mt-3 text-xs font-medium text-neutral-500">
                            <span className="flex items-center gap-1">
                                Risk: <span className={item.risk === 'Low' ? 'text-green-400' : 'text-yellow-400'}>{item.risk}</span>
                            </span>
                            <span>Resource: <code className="bg-neutral-900 px-1 py-0.5 rounded text-neutral-300">{item.resource_id}</code></span>
                        </div>
                    </div>
                </div>

                {/* Right Actions */}
                <div className="flex flex-row sm:flex-col items-end justify-between sm:justify-center gap-3 w-full sm:w-auto mt-2 sm:mt-0 pl-12 sm:pl-0">
                    <div className="text-right">
                        <p className="text-xs text-neutral-500 uppercase">Save</p>
                        <p className="text-lg font-bold text-green-400">${item.monthly_savings}<span className="text-sm font-normal text-neutral-500">/mo</span></p>
                    </div>

                    {status === 'pending' && (
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => setStatus('dismissed')}
                                className="p-2 text-neutral-500 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors"
                                title="Dismiss"
                            >
                                <Trash2 className="w-4 h-4" />
                            </button>
                            <button className="p-2 text-neutral-500 hover:text-white hover:bg-white/10 rounded transition-colors" title="Details">
                                <Info className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() => setStatus('applied')}
                                className="px-3 py-1.5 bg-accent-dark hover:bg-accent-light text-white text-sm font-medium rounded shadow-lg hover:shadow-accent-dark/20 transition-all flex items-center gap-2"
                            >
                                <Check className="w-3 h-3" /> Apply
                            </button>
                        </div>
                    )}
                    {status === 'applied' && (
                        <span className="text-sm text-green-500 font-medium flex items-center gap-1">
                            Applied <Check className="w-3 h-3" />
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
};

export default function AuditRecommendations({ recommendations }) {
    return (
        <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground mb-4">Recommended Actions</h3>
            {recommendations.map(rec => (
                <RecommendationItem key={rec.id} item={rec} />
            ))}
        </div>
    );
}

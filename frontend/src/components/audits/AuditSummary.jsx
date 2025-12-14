"use client";
import React from "react";
import { Clock, CheckCircle2, DollarSign, Search, AlertOctagon } from "lucide-react";

export default function AuditSummary({ data }) {
    if (!data) return null;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
            <div className="bg-card border border-border-light rounded-xl p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-neutral-400 uppercase font-medium">Audit ID</span>
                    <AlertOctagon className="w-4 h-4 text-neutral-500" />
                </div>
                <div>
                    <p className="text-lg font-bold text-foreground truncate" title={data.audit_id}>{data.audit_id}</p>
                    <p className="text-xs text-neutral-500 mt-1">{new Date(data.timestamp).toLocaleDateString()}</p>
                </div>
            </div>

            <div className="bg-card border border-border-light rounded-xl p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-neutral-400 uppercase font-medium">Duration</span>
                    <Clock className="w-4 h-4 text-neutral-500" />
                </div>
                <div className="flex items-end gap-2">
                    <p className="text-2xl font-bold text-foreground">{data.duration_seconds}s</p>
                </div>
            </div>

            <div className="bg-card border border-border-light rounded-xl p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-neutral-400 uppercase font-medium">Scanned</span>
                    <Search className="w-4 h-4 text-neutral-500" />
                </div>
                <div>
                    <p className="text-2xl font-bold text-foreground">{data.resources_scanned}</p>
                    <p className="text-xs text-neutral-500 mt-1">Resources</p>
                </div>
            </div>

            <div className="bg-card border border-border-light rounded-xl p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-neutral-400 uppercase font-medium">Issues Found</span>
                    <AlertOctagon className="w-4 h-4 text-accent-light" />
                </div>
                <div className="flex items-end gap-2">
                    <p className="text-2xl font-bold text-accent-light">{data.issues_found}</p>
                </div>
            </div>

            <div className="bg-card border border-border-light rounded-xl p-4 flex flex-col justify-between bg-gradient-to-br from-[#141414] to-green-900/10">
                <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-green-400 uppercase font-medium">Potential Savings</span>
                    <DollarSign className="w-4 h-4 text-green-500" />
                </div>
                <div>
                    <p className="text-2xl font-bold text-green-400">${data.total_savings}<span className="text-sm font-normal text-green-500/70">/mo</span></p>
                </div>
            </div>
        </div>
    );
}

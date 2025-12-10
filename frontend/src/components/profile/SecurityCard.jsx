"use client";
import React from "react";
import { ShieldCheck, Lock, ExternalLink } from "lucide-react";

export default function SecurityCard() {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm h-full">
            <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-accent-light" />
                Security
            </h3>

            <div className="space-y-4">
                <div className="p-4 bg-[#1a1a1a] rounded-lg border border-neutral-800 flex items-center justify-between">
                    <div>
                        <p className="text-sm font-medium text-foreground flex items-center gap-2">
                            <Lock className="w-4 h-4 text-neutral-400" /> Password
                        </p>
                        <p className="text-xs text-neutral-500 mt-1">Last changed 30 days ago</p>
                    </div>
                    <button className="px-3 py-1.5 text-xs font-medium text-neutral-300 bg-neutral-800 hover:bg-neutral-700 rounded border border-neutral-700 transition-colors">
                        Change
                    </button>
                </div>

                <div className="p-4 bg-[#1a1a1a] rounded-lg border border-neutral-800 flex items-center justify-between">
                    <div>
                        <p className="text-sm font-medium text-foreground flex items-center gap-2">
                            <ShieldCheck className="w-4 h-4 text-green-500" /> 2-Factor Auth
                        </p>
                        <p className="text-xs text-neutral-500 mt-1">Currently enabled</p>
                    </div>
                    <span className="px-2 py-1 text-xs font-bold text-green-500 bg-green-500/10 border border-green-500/20 rounded">
                        Enabled
                    </span>
                </div>

                <div className="pt-2">
                    <a href="#" className="text-xs text-accent-light hover:underline flex items-center gap-1">
                        View active sessions <ExternalLink className="w-3 h-3" />
                    </a>
                </div>
            </div>
        </div>
    );
}

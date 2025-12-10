"use client";
import React from "react";
import { Download, Mail } from "lucide-react";

export default function ExportSettings() {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-2">
                <Download className="w-5 h-5 text-accent-light" />
                Export Settings
            </h3>

            <div className="space-y-6">
                <div className="space-y-2">
                    <label className="block text-sm font-medium text-neutral-400">
                        Default Report Format
                    </label>
                    <div className="grid grid-cols-3 gap-3">
                        <button className="px-4 py-2 bg-neutral-800 border-2 border-accent-dark text-white rounded-lg text-sm font-medium">PDF</button>
                        <button className="px-4 py-2 bg-[#1a1a1a] border border-neutral-800 text-neutral-400 hover:bg-neutral-800 rounded-lg text-sm font-medium transition-colors">CSV</button>
                        <button className="px-4 py-2 bg-[#1a1a1a] border border-neutral-800 text-neutral-400 hover:bg-neutral-800 rounded-lg text-sm font-medium transition-colors">JSON</button>
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="block text-sm font-medium text-neutral-400">
                        Automatically Email Reports To
                    </label>
                    <div className="relative">
                        <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-500" />
                        <input
                            type="email"
                            placeholder="team@example.com"
                            className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg pl-10 pr-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all placeholder:text-neutral-600"
                        />
                    </div>
                    <p className="text-xs text-neutral-500">Separate multiple emails with commas.</p>
                </div>
            </div>
        </div>
    );
}

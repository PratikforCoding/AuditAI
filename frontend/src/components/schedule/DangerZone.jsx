"use client";
import React from "react";
import { Trash2, RefreshCcw, Unplug, AlertOctagon } from "lucide-react";

export default function DangerZone() {
    return (
        <div className="bg-card border border-red-900/30 rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-red-500 mb-6 flex items-center gap-2">
                <AlertOctagon className="w-5 h-5" />
                Danger Zone
            </h3>

            <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 border border-red-900/30 rounded-lg bg-red-950/10 gap-4">
                    <div>
                        <h4 className="font-medium text-foreground">Reset All Recommendations</h4>
                        <p className="text-sm text-neutral-400">
                            Clear all current optimization suggestions. They will be regenerated on the next audit.
                        </p>
                    </div>
                    <button className="px-4 py-2 bg-red-900/20 hover:bg-red-900/40 text-red-400 border border-red-900/50 rounded-lg text-sm font-medium transition-colors flex items-center whitespace-nowrap">
                        <RefreshCcw className="w-4 h-4 mr-2" />
                        Reset Data
                    </button>
                </div>

                <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 border border-red-900/30 rounded-lg bg-red-950/10 gap-4">
                    <div>
                        <h4 className="font-medium text-foreground">Delete Audit History</h4>
                        <p className="text-sm text-neutral-400">
                            Permanently remove all past audit logs and reports. This action cannot be undone.
                        </p>
                    </div>
                    <button className="px-4 py-2 bg-red-900/20 hover:bg-red-900/40 text-red-400 border border-red-900/50 rounded-lg text-sm font-medium transition-colors flex items-center whitespace-nowrap">
                        <Trash2 className="w-4 h-4 mr-2" />
                        Delete History
                    </button>
                </div>

                <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 border border-red-900/30 rounded-lg bg-red-950/10 gap-4">
                    <div>
                        <h4 className="font-medium text-foreground">Disconnect GCP Account</h4>
                        <p className="text-sm text-neutral-400">
                            Revoke access to your Google Cloud Platform account. Monitoring will stop immediately.
                        </p>
                    </div>
                    <button className="px-4 py-2 bg-red-900/20 hover:bg-red-900/40 text-red-400 border border-red-900/50 rounded-lg text-sm font-medium transition-colors flex items-center whitespace-nowrap">
                        <Unplug className="w-4 h-4 mr-2" />
                        Disconnect
                    </button>
                </div>
            </div>
        </div>
    );
}

"use client";
import React from "react";
import { Bell, Mail } from "lucide-react";

export default function NotificationsSettings() {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-2">
                <Bell className="w-5 h-5 text-accent-light" />
                Notifications
            </h3>

            <div className="space-y-4">
                <div className="flex items-start space-x-3 p-3 hover:bg-neutral-900/40 rounded-lg transition-colors">
                    <input
                        type="checkbox"
                        id="notify-critical"
                        className="mt-1 w-4 h-4 rounded border-neutral-700 bg-neutral-800 text-accent-dark focus:ring-accent-dark/50"
                        defaultChecked
                    />
                    <label htmlFor="notify-critical" className="text-sm">
                        <span className="block font-medium text-foreground">Critical Issues</span>
                        <span className="block text-neutral-500">
                            Receive emails immediately when critical cost spikes or security risks are detected.
                        </span>
                    </label>
                </div>

                <div className="flex items-start space-x-3 p-3 hover:bg-neutral-900/40 rounded-lg transition-colors">
                    <input
                        type="checkbox"
                        id="notify-completion"
                        className="mt-1 w-4 h-4 rounded border-neutral-700 bg-neutral-800 text-accent-dark focus:ring-accent-dark/50"
                        defaultChecked
                    />
                    <label htmlFor="notify-completion" className="text-sm">
                        <span className="block font-medium text-foreground">Audit Completion</span>
                        <span className="block text-neutral-500">
                            Get notified when a scheduled audit finishes successfully.
                        </span>
                    </label>
                </div>

                <div className="flex items-start space-x-3 p-3 hover:bg-neutral-900/40 rounded-lg transition-colors">
                    <input
                        type="checkbox"
                        id="notify-weekly"
                        className="mt-1 w-4 h-4 rounded border-neutral-700 bg-neutral-800 text-accent-dark focus:ring-accent-dark/50"
                    />
                    <label htmlFor="notify-weekly" className="text-sm">
                        <span className="block font-medium text-foreground">Weekly Summary</span>
                        <span className="block text-neutral-500">
                            Receive a weekly digest of cost trends and savings opportunities.
                        </span>
                    </label>
                </div>

                <hr className="border-neutral-800 my-4" />

                <div className="space-y-3">
                    <h4 className="text-sm font-semibold text-neutral-300 mb-2">Integrations</h4>
                    <div className="flex items-center justify-between p-3 border border-neutral-800 rounded-lg bg-[#1a1a1a]">
                        <div className="flex items-center gap-3">
                            {/* Slack Icon Placeholder */}
                            <div className="w-8 h-8 bg-[#4A154B] rounded-md flex items-center justify-center text-white font-bold text-xs">Sl</div>
                            <span className="text-sm font-medium text-foreground">Slack Notifications</span>
                        </div>
                        <button className="text-xs px-3 py-1.5 bg-neutral-800 hover:bg-neutral-700 border border-neutral-700 rounded-md transition-colors text-neutral-300">
                            Connect
                        </button>
                    </div>
                    <div className="flex items-center justify-between p-3 border border-neutral-800 rounded-lg bg-[#1a1a1a]">
                        <div className="flex items-center gap-3">
                            {/* Discord Icon Placeholder */}
                            <div className="w-8 h-8 bg-[#5865F2] rounded-md flex items-center justify-center text-white font-bold text-xs">Di</div>
                            <span className="text-sm font-medium text-foreground">Discord Webhook</span>
                        </div>
                        <button className="text-xs px-3 py-1.5 bg-neutral-800 hover:bg-neutral-700 border border-neutral-700 rounded-md transition-colors text-neutral-300">
                            Connect
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

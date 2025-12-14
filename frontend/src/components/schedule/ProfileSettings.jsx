"use client";
import React from "react";
import { User, Lock, Key, ShieldCheck } from "lucide-react";

export default function ProfileSettings() {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-2">
                <User className="w-5 h-5 text-accent-light" />
                Account & Security
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Profile Info */}
                <div className="space-y-4">
                    <h4 className="text-base font-semibold text-neutral-300 flex items-center gap-2">
                        <User className="w-4 h-4 text-neutral-500" />
                        Profile Information
                    </h4>
                    <div className="space-y-3">
                        <div>
                            <label className="block text-xs font-medium text-neutral-500 mb-1">
                                Full Name
                            </label>
                            <input
                                type="text"
                                defaultValue="Audit User"
                                className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-3 py-2 text-sm text-foreground focus:ring-1 focus:ring-accent-dark outline-none"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-medium text-neutral-500 mb-1">
                                Email Address
                            </label>
                            <input
                                type="email"
                                defaultValue="user@auditai.com"
                                className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-3 py-2 text-sm text-foreground focus:ring-1 focus:ring-accent-dark outline-none"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-medium text-neutral-500 mb-1">
                                GCP Project ID
                            </label>
                            <input
                                type="text"
                                defaultValue="serious-projects-123"
                                disabled
                                className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-3 py-2 text-sm text-neutral-400 cursor-not-allowed"
                            />
                        </div>
                    </div>
                </div>

                {/* Security */}
                <div className="space-y-4">
                    <h4 className="text-base font-semibold text-neutral-300 flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4 text-neutral-500" />
                        Security
                    </h4>

                    <div className="space-y-3">
                        <button className="w-full flex items-center justify-between p-3 bg-[#1a1a1a] border border-neutral-800 rounded-lg hover:border-neutral-600 transition-colors group">
                            <span className="flex items-center gap-3 text-sm text-foreground">
                                <Lock className="w-4 h-4 text-neutral-400 group-hover:text-accent-light transition-colors" />
                                Change Password
                            </span>
                            <span className="text-xs text-neutral-500">Last changed 30 days ago</span>
                        </button>

                        <button className="w-full flex items-center justify-between p-3 bg-[#1a1a1a] border border-neutral-800 rounded-lg hover:border-neutral-600 transition-colors group">
                            <span className="flex items-center gap-3 text-sm text-foreground">
                                <Key className="w-4 h-4 text-neutral-400 group-hover:text-accent-light transition-colors" />
                                API Keys
                            </span>
                            <span className="text-xs text-neutral-500">2 Active Keys</span>
                        </button>

                        <div className="flex items-center justify-between p-3 bg-[#1a1a1a] border border-neutral-800 rounded-lg">
                            <span className="flex items-center gap-3 text-sm text-foreground">
                                <ShieldCheck className="w-4 h-4 text-green-500" />
                                Two-Factor Auth
                            </span>
                            <span className="px-2 py-0.5 bg-green-500/10 text-green-500 text-xs font-medium rounded border border-green-500/20">Enabled</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

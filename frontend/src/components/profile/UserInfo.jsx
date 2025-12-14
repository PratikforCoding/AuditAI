"use client";
import React, { useState } from "react";
import { User, Save } from "lucide-react";

export default function UserInfo() {
    const [isSaving, setIsSaving] = useState(false);

    const handleSave = async () => {
        setIsSaving(true);
        await new Promise(resolve => setTimeout(resolve, 1000));
        setIsSaving(false);
        // In real app, toast success
    };

    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                <User className="w-5 h-5 text-accent-light" />
                Personal Information
            </h3>
            
            <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                    <p className="text-xs text-neutral-600 mt-1">Project ID cannot be changed here.</p>
                </div>

                <div className="flex justify-end pt-2">
                     <button
                        onClick={handleSave}
                        disabled={isSaving}
                        className={`flex items-center px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-white rounded-lg text-sm font-medium transition-all ${isSaving ? "opacity-70 cursor-not-allowed" : ""}`}
                    >
                        {isSaving ? (
                            <>
                                <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                                Saving...
                            </>
                        ) : (
                            <>
                                <Save className="w-4 h-4 mr-2" />
                                Save Profile
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
